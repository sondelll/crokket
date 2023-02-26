import customtkinter as ctk
from customtkinter import filedialog
from tkinter import StringVar

from typing import Optional, Union, Tuple

from ..runtime_utils import ensure_data_folder
from ...core.recognize import CrokketRecognition
from ...core.io import TextOut, filename_cleanup

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")

MODEL_LOOKUP = {
    "Tiny": "openai/whisper-tiny",
    "Small": "openai/whisper-small",
    "Medium": "openai/whisper-medium",
    "Large": "openai/whisper-large-v2",
}


class FileSelectionArea(ctk.CTkFrame):
    def __init__(
        self,
        master: any,
        width: int = 200,
        height: int = 200,
        corner_radius: Optional[Union[int, str]] = None,
        border_width: Optional[Union[int, str]] = None,
        bg_color: Union[str, Tuple[str, str]] = "transparent",
        fg_color: Optional[Union[str, Tuple[str, str]]] = None,
        border_color: Optional[Union[str, Tuple[str, str]]] = None,
        background_corner_colors: Union[
            Tuple[Union[str, Tuple[str, str]]], None
        ] = None,
        overwrite_preferred_drawing_method: Union[str, None] = None,
        **kwargs
    ):
        super().__init__(
            master,
            width,
            height,
            corner_radius,
            border_width,
            bg_color,
            fg_color,
            border_color,
            background_corner_colors,
            overwrite_preferred_drawing_method,
            **kwargs
        )
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0), weight=1)

        self.path_box = ctk.CTkEntry(master=self)
        
        self.path_box.grid(row=0, column=0, padx=2, pady=8, sticky="nsew")

        self.browse_button = ctk.CTkButton(master=self, text="Browse", command=self.on_browse)
        self.browse_button.grid(row=0, column=1, padx=2, pady=8, sticky="nsew")

    def on_browse(self):
        path_select = filedialog.askopenfilename()
        try:
            self.path_box.delete(0, len(self.path_box.get()))
        except:
            pass # Yeah yeah go cry about it.
        self.path_box.insert(0, path_select)


class RunProcessingArea(ctk.CTkFrame):
    def __init__(
        self,
        path_fn_ref,
        master: any,
        width: int = 200,
        height: int = 200,
        corner_radius: Optional[Union[int, str]] = None,
        border_width: Optional[Union[int, str]] = None,
        bg_color: Union[str, Tuple[str, str]] = "transparent",
        fg_color: Optional[Union[str, Tuple[str, str]]] = None,
        border_color: Optional[Union[str, Tuple[str, str]]] = None,
        background_corner_colors: Union[
            Tuple[Union[str, Tuple[str, str]]], None
        ] = None,
        overwrite_preferred_drawing_method: Union[str, None] = None,
        **kwargs
    ):
        super().__init__(
            master,
            width,
            height,
            corner_radius,
            border_width,
            bg_color,
            fg_color,
            border_color,
            background_corner_colors,
            overwrite_preferred_drawing_method,
            **kwargs
        )
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0), weight=1)
        self.path_fn = path_fn_ref
        self.model_selection = ctk.CTkOptionMenu(
            master=self, values=["Tiny", "Small", "Medium", "Large"]
        )
        self.model_selection.grid(row=0, column=0, padx=2, pady=8, sticky="nsew")
        self.run_button = ctk.CTkButton(master=self, text="Run", command=self._process)
        self.run_button.grid(row=0, column=1, padx=2, pady=8, sticky="nsew")
    
    def _process(self):
        import threading
        p = self.path_fn()
        _model = MODEL_LOOKUP[self.model_selection.get()]
        ensure_data_folder()
        print("Transcribing audio, this can take a couple of minutes..\n")
        
        def aside(p:str, _model:str) -> None:
            cr = CrokketRecognition(p, _model)
            outvar = cr.transcript()
            clean_name = filename_cleanup(p)
            out = TextOut(clean_name, outvar)
            out.write()
            print(f"Transcribing done")
            return {}

        t = threading.Thread(target=aside, args=(p, _model))
        t.start()


class InteractiveArea(ctk.CTkFrame):
    def __init__(
        self,
        master: any,
        width: int = 200,
        height: int = 200,
        corner_radius: Optional[Union[int, str]] = None,
        border_width: Optional[Union[int, str]] = None,
        bg_color: Union[str, Tuple[str, str]] = "transparent",
        fg_color: Optional[Union[str, Tuple[str, str]]] = None,
        border_color: Optional[Union[str, Tuple[str, str]]] = None,
        background_corner_colors: Union[
            Tuple[Union[str, Tuple[str, str]]], None
        ] = None,
        overwrite_preferred_drawing_method: Union[str, None] = None,
        **kwargs
    ):
        super().__init__(
            master,
            width,
            height,
            corner_radius,
            border_width,
            bg_color,
            fg_color,
            border_color,
            background_corner_colors,
            overwrite_preferred_drawing_method,
            **kwargs
        )
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((1, 2), weight=1)
        self._bg_color = "transparent"
        self.fise = FileSelectionArea(self, fg_color="transparent")
        self.fise.grid(row=1, column=0, sticky="new")
        self.rupr = RunProcessingArea(self.get_filepath, master=self, fg_color="transparent")
        self.rupr.grid(row=2, column=0, sticky="sew")
    
    def get_filepath(self):
        return self.fise.path_box.get()

class CrokketGUIApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.wm_title("Crokket")
        self.minsize(480, 320)


        self.title_label = ctk.CTkLabel(
            master=self,
            text="Crokket",
            font=ctk.CTkFont(size=28, weight="bold", family="verdana"),
            anchor="nw",
        )
        self.title_label.grid(row=0, column=0, padx=16, pady=8)

        self.inter = InteractiveArea(master=self, fg_color="transparent")
        self.inter.grid(row=1, column=1, sticky="nsew", padx=16, pady=8)
