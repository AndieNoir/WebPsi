WebPsi
======

A Python web app to aid psychic abilities experiments.

Running
-------

1. WebPsi supports both local and remote random number generation. For local, install [ComScire driver](https://comscire.com/downloads/).
   For remote, run [Quanttp](https://github.com/awasisto/quanttp) on the remote machine and set `QUANTTP_LOCATION`
   environment variable
   
   Example:

   ```
   # Windows
   set QUANTTP_LOCATION=192.168.0.136:8080/quanttp

   # Linux
   export QUANTTP_LOCATION=192.168.0.136:8080/quanttp
   ```

2. Run the following commands

   ```
   pip3 install -r requirements.txt
   python3 -m webpsi
   ```

3. Open http://localhost:58700

Adding a new random number generator
------------------------------------

1.  Create a class that extends `Generator` and override the `get_bytes` method

    Example:

    ```python
    # webpsi/generator/dev_hwrng.py
    
    from webpsi.generator.base import Generator
    
    
    class DevHwrng(Generator, id='my_rng', bit_numbering=BitNumbering.BitNumbering.UNKNOWN):
    
       def get_bytes(self, length):
           with open('/dev/hwrng', 'rb') as f:
               return f.read(length)
    ```

2.  Set the generator class on `config.py`

    ```python
    # webpsi/config.py
    
    from webpsi.generator.dev_hwrng import DevHwrng
    
    
    GENERATOR_CLASS = DevHwrng
    ```

License
-------

    Copyright (C) 2020 AndieNoir
    
    WebPsi is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    WebPsi is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with WebPsi.  If not, see <https://www.gnu.org/licenses/>.
