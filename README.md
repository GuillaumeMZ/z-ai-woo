# zAIwoo

An AI-based aimbot for CS:GO.

## How to install/run

- Download and install [Visual Studio 2022](https://visualstudio.microsoft.com/) (Be sure to check the "desktop development with C++" module)
- Download and install [Python](https://www.python.org/)
- Download and install [CUDA](https://developer.nvidia.com/cuda-toolkit)
- Download and install [cuDNN](https://developer.nvidia.com/cudnn)
- Clone this repository and open a terminal inside it
- Create a virtual environment:

    ```powershell
    py -m venv venv
    ```

- Load the virtual environment:

    ```powershell
    .\venv\Scripts\activate
    ```

- Download a CUDA-compatible PyTorch:

    ```powershell
    py -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
    ```

- Install the dependencies:

    ```powershell
    py -m pip install -r requirements.txt
    ```

- Run the program:

    ```powershell
    py zaiwoo.py
    ```

## Caveats

- Currently, CS:GO must be run in fullscreen on the main monitor for zAIwoo to work properly. Also, zAIwoo doesn't work with multi-monitor setups. This will be addressed in the future.
- zAIwoo is slow. This will be addressed in the future.
