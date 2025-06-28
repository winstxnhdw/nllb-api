from fasttext.FastText import load_model as load_model

class FastText:
    def loadModel(self, model_path: str) -> None: ...  # noqa: N802
    def predict(self, text: str, k: int, threshold: float, on_unicode_error: str) -> list[tuple[float, str]]: ...

def fasttext() -> FastText: ...
