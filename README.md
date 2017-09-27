# Python script for Duke MTMC

Duke MTMC download can be made through a Matlab script. This is a conversion of the code in python.

The file is a bit more "complex" in its structure because I wanted to have more options (download specific parts, extract the frames in a specific video format, etc.).

## How to use it

The simplest way to use the script is by doing the following in a terminal

```bash
python script.py
```

This will import all the Duke MTMC dataset into the current folder.

2 options are given to the script :
 * **-d** or **-destination**, to provide a destination folder for the dataset. As explained earlier, the dataset is extracted by default to the current folder. The option is let to the user to define a destination folder.
 ```bash
 python script.py -d ./test
 ```
 * **-p** or **-params**, to use specipic parameters. The value to give is the path to a JSON used to tweak the parameters. Further details on the structure of this file and the values that can be modified are given in the next section. You can try and test with the given JSON file.
 ```bash
 python python.py -p ./example.json
 ```
 * **-v** or **--verbose**, for verbose running.
 ```bash
 $ python python.py -v
 Patience, this may take 1-2 days!
 Creating folder structure...
 Downloading data...
 ```

## How to tweak it

A JSON file can be used to modify the parameters for the extraction.
