import numpy as np

from torch.nn import AvgPool1d
from torch import Tensor

INT32_MAX = 4294967295
SMOOTHING = 6


class SplitTimes:
    def __init__(
        self,
        audio_obj:tuple,
        threshold:float = 0.0125,
        step_size_seconds:float = 0.25,
        silence_margin:float = 0.5,
        verbose_mode:bool = False
    ) -> None:
        self.verbose_mode = verbose_mode
        self.audio:np.ndarray = audio_obj[1]
        
        if isinstance(np.max(self.audio), np.int32):
            self.audio = _int32_conversion(self.audio)  
        
        self.audio = _amplitude_normalize(self.audio)
        
        self.split_indices = []

        self._sample_rate = audio_obj[0]
        self._threshold = threshold
        
        self._step_size = step_size_seconds
        self._margin = silence_margin
        
        if verbose_mode:
            print("Sample max:", max(self.audio.min(), self.audio.max()))
            print("Sample min:", min(self.audio.min(), self.audio.max()))
        
        self._generate_split_points()
      
    def get_splits(self):
        return self.split_indices
      
    def _generate_split_points(self):
        for timestep in range(
            0,
            len(self.audio),
            int(self._step_size*self._sample_rate)
        ):
            if timestep > len(self.audio):
                break
            
            if self._is_quiet_window(timestep, samples_radius=int(self._sample_rate*self._margin/SMOOTHING)):
                self.split_indices.append(timestep*SMOOTHING)

    def _is_quiet_window(
        self,
        step_n:int,
        samples_radius:int
    ) -> bool:
        """Checks on both sides of step_n to see if split is suitable.

        Args:
            step_n (int): The timestep in the audio
            min_sec (float, optional): Length to qualify as a quiet window. Defaults to 1.5.
            samples_radius(int): How many samples before and after the timestep to measure
        Returns:
            bool: Whether the timestep is a quiet window.
        """
        if np.average(self.audio[step_n]) > self._threshold:
            if self.verbose_mode:
                print(f"Above threshold at sample {step_n}")
            return False
        if step_n + samples_radius > len(self.audio):
            if self.verbose_mode:
                print(f"Border range return")
            return False
        
        for _n in range(samples_radius, 0, -2):
            backstepped = self.audio[step_n-_n]
            forwardstepped = self.audio[step_n+_n]
            
            if np.average(forwardstepped) > self._threshold:
                if self.verbose_mode:
                    print(f"Tail above threshold at sample {step_n+_n}")
                return False
            
            if np.average(backstepped) > self._threshold:
                if self.verbose_mode:
                    print(f"Nose above threshold at sample {step_n-_n}")
                return False
        if self.verbose_mode:
            print(f"Quiet window around {step_n}")
        return True


def _int32_conversion(audio:np.ndarray):
    audio = audio.astype(np.float32)
    audio = np.divide(audio, INT32_MAX/2)
    
    #audio_max = max(audio.min(), audio.max())
    #audio = np.subtract(audio, audio_max)
    audio = Tensor(audio)
    audio:Tensor = AvgPool1d([SMOOTHING], [SMOOTHING])(audio.unsqueeze(0))
    audio = audio.squeeze().numpy()
    
    return audio


def _amplitude_normalize(audio:np.ndarray) -> np.ndarray:
    peak = max(audio.min(), audio.max())
    audio = np.subtract(audio, peak)
    
    anti_peak = min(audio.min(), audio.max())
    audio = np.multiply(audio, abs(1/anti_peak))
    audio = np.subtract(audio, np.mean(audio))
    audio = np.abs(audio)
    
    return audio
