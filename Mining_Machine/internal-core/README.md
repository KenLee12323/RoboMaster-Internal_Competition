# RM2020 Internal Competition Code Base

> There will be drivers update to this repo later.
> 
> Please clone this instead of downloading a zip.

* Board: STM32F103C8 (BluePill)
* OS: ChibiOS
* Debugger: JLink
* Compiler toolchain: Arm GNU toolchain (2017 Q2)

## Directory Structure
* `board`: Board hardware configuration
* `build`: Build output (the output elf is `RM20.elf`)
* `chibios`: ChibiOS library (RTOS). [Documentation](http://www.chibios.org/dokuwiki/doku.php?id=chibios:documentation:start)
* `CMSIS`: CMSIS library 
* `config`: ChibiOS config
* `datasheets`: Datasheets useful for development
* `openocd`: OpenOCD scripts
* `src`: User source code

## Compile
> All commands here should be run in the project directory, not inside `src`.

```
make
```

* `make -j` could make compilation process faster by utilizing multiple core on your computer.
* `make clean` could clear the `.dep` directory and `build` directory. Use it when there are myterious errors such as `cannot find source file for ...`. You can search the web or ask seniors for the detailed reasons behind.

## General Environment Setup
* Install [GNU Arm toolchain](https://developer.arm.com/tools-and-software/open-source-software/developer-tools/gnu-toolchain/gnu-rm/downloads) **2017 Q2**
* Install [Segger Ozone](https://www.segger.com/downloads/jlink/#Ozone)

### Windows Specific

* When installing arm toolchain, please add it to your path.
* Install [MSYS2](https://www.msys2.org/) and add the `C:\msys64\usr\bin` to your path. (assuming you install it in `C:\msys64`)
* Run the following command in MSYS2:
    ```bash
    pacman -S make
    ```

### Unix System (Linux and Mac)

1. Download Linux/Mac 64-bit GNU Arm toolchain 2017 Q2
2. Unpack it (`tar -xjf`) into current directory (make sure it is in an empty directory)
3. Add the path in your `~/.bashrc` or `~/.zshrc`:

   ```bash
   export PATH=$PATH:(path to bin directory of the file)
   ```

   Example:

   ```bash
   export PATH=$PATH:$HOME/arm-gcc-2017-q2/bin
   ```

## Configuring VSCode
You can configure VSCode to get a IDE-like experience, including autocomplete function, diagnostics, goto definition etc.

We can tell the extension all necessary configurations through **compilation database**.

1.  Install Python3.
2.  Install [compiledb](https://github.com/nickdiego/compiledb). Install using the command `pip3 install --user compiledb` to avoid permission problem.
    > Note that for Windows users, you may have to configure the path variable. Usually the path is in `%APPDATA%/Python/Python37/Scripts` for Python3.7.
3.  Run `compiledb <make command>`, such as `compiledb make -j`, and it would compile the project and generate the compilation database for you.
4.  Configure `c_cpp_properties.json` by opening the command panel, type `C/C++ Edit Configuration`, 
    select `C/C++: Edit Configurations (JSON)`, and change the content to:
    ```json
    {
        "configurations": [
            {
                "name": "ARM",
                "compileCommands": "${workspaceFolder}/compile_commands.json",
                "cStandard": "c11",
                "cppStandard": "c++17"
            }
        ],
        "version": 4
    }
    ```

### ccls
If you want more, you can check out [ccls](https://github.com/MaskRay/ccls).

