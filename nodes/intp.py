import random

class any_io_type(str):
    def __ne__(self, __value: object) -> bool:  # pragma: no cover - trivial
        return False

CONTROL_MODES = ["fixed", "increment", "decrement", "random_seed"]
MAX_INT = 1115899906842624

class INTPlus:
    
    SIGNAL = any_io_type("*")

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "int": ("INT", {"default": 0, "min": -MAX_INT, "max": MAX_INT}),
                "control_mode": (CONTROL_MODES, {"default": "fixed"}),
                "invert": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "signal": (INTPlus.SIGNAL,),
            },
            "hidden": {
                "unique_id": "UNIQUE_ID",
            },
        }
    
    RETURN_TYPES = ("INT",)
    RETURN_NAMES = ("int",)
    OUTPUT_NODE = True
    FUNCTION = "execute"
    CATEGORY = "LumyLogic/Primitive+"

    def execute(self, int, control_mode, invert, signal=None, unique_id=None):
        # Determine if we should apply control
        # Treat None and False the same way
        signal_inactive = signal is None or (isinstance(signal, bool) and signal is False)
        apply_control = signal_inactive if invert else not signal_inactive
        
        output_value = int
        
        if apply_control and control_mode != "fixed":
            if control_mode == "increment":
                output_value = int + 1
                if output_value > MAX_INT:
                    output_value = -MAX_INT
            elif control_mode == "decrement":
                output_value = int - 1
                if output_value < -MAX_INT:
                    output_value = MAX_INT
            elif control_mode == "random_seed":
                output_value = random.randint(1, MAX_INT)
        
        return {"ui": {"value": [output_value]}, "result": (output_value,)}
    
INTP_CLASS_MAPPING = {
    "INTPlus": INTPlus,
}
INTP_DISPLAY_NAME_MAPPINGS = {
    "INTPlus": "int+",
}
