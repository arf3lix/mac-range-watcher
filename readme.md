# How to install mac-address-watcher

## install python on offline computer

run phython setup exe, follow instructions and check add python to path 

## Install Dependencies

### move to mac-range-watcher path

```
cd path/to/mac-range-watcher
```

###  install dependencies:

```
pip install --no-index --find-links deps -r requirements.txt
```

###  modify mac_address_watcher.bat:

if python was correctly installed, run following command to get python installation path:

```
python -c "import sys; print(sys.executable)"
```

copy and paste the resulting path into mac_address_watcher.bat, put instead of `C:\ruta\a\python.exe` and instead of `C:\ruta\al\script\mi_script.py` put the absolute path of `mac-range-watcher\main.py`

### setup config.ini

here you need to put path to the folder where trackmac.csv is located

put the current mac address range

and setup the limit values for each message alert