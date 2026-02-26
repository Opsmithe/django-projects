command to install python dependency manager uv
```curl -LsSf https://astral.sh/uv/install.sh | sh ``

add uv to path and check version
```export PATH="$HOME/.local/bin:$PATH" && uv --version```

create virtual environment using uv
```uv venv venv```
*install django using uv*
```uv pip install django```

using pip
*pip is pre-installed as a library in python3*
*create a virtual environment*
```python3 -m venv <myvenv>```
**replace <myvenv> with your desired virtual env name**
*activate virtual environment(myvenv)*
```source ./<myvenv>/bin/activate```
*install django*
```python3 -m pip install django```
*start a django-project*
**replace <project_name> with your desired project name**
```django-admin startproject <project_name>```


