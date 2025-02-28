import time
from typing import Any, Callable, Dict


class Model:
    def train(
        self, num_epochs: int, progress_callback: Callable[[Dict[str, Any]], None]
    ):
        for i in range(num_epochs):
            time.sleep(0.2)
            metrics = {
                "progress": round((i + 1) / num_epochs, 3),
                "charts": {
                    "accuracy": {
                        "x": i + 1,
                        "y": {
                            "train": round(0.8 + (i + 1) * 0.1 / num_epochs, 3),
                            "validation": round(0.6 + (i + 1) * 0.2 / num_epochs, 3),
                        },
                    },
                    "loss": {
                        "x": i + 1,
                        "y": {
                            "train": round(0.8 - (i + 1) * 0.7 / num_epochs, 3),
                            "validation": round(0.9 - (i + 1) * 0.6 / num_epochs, 3),
                        },
                    }
                },
            }
            progress_callback(metrics)
            
    def predict(self, x):
        return x * 2
    
    def load(self, path):
        print(f"Loaded: {path}")
        return self