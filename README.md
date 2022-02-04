# IR_System

CS336.M11.KHCL Final Project.

This project is build based on Python and Django Platform.

## 1. Installation


Both windows, macos and linux operating systems work well with this project.

Recommended working environment:
- tensorflow >= 2.7.0
- python3.8


* [1.1. Python Environment Setup](#1)
* [1.2. Project clone](#2)
* [1.3. Install tensorflow and third-party libraries](#3)

<a name="1"></a>

### 1.1. Python Environment Setup

- Python download

    - You can download python at this link: https://www.python.org/downloads/

- Create virtual environment

    - Install virtualenv
        ```bash
        python3 -m pip install virtualenv
        ```

    - Create a new virtual environment
        ```bash
        python3 -m virtualenv my_env
        ```

        This command will create an virtual environment named **my_env** with your python version.

    - To activate the virtual environment you just created, enter the following command at the command line.
        
        For Window:
        ```shell
        .\my_env\Scripts\activate
        ```

        For MacOS and Linux:
        ```shell
        source .my_env/bin/activate
        ```

    The above python environment are installed.

<a name="2"></a>

### 1.2. Project Clone

Clone project repo with the following command.

```bash
git clone https://github.com/thanhnhan311201/IR_System.git
```

<a name="3"></a>

### 1.3. Install tensorflow and third-party libraries

Please run the following command to install.

```bash
cd IR_System
python3 -m pip install -r requirements.txt
```

## 2. Dataset Preparation


### 2.1. Download dataset images

- You can download dataset images with this [link](https://www.robots.ox.ac.uk/~vgg/data/oxbuildings/oxbuild_images.tgz)

- Then you need to extract and put it in folder ```static/datasets/```

```
IR_System
└───IRsystem_WebPage
        └───static
                └───datasets
                        └───oxbuild_dataset
                                └───images
                                        │all_souls_000000.jpg
                                        │all_souls_000001.jpg
                                        │all_souls_000002.jpg
                                        |...
```

### 2.2. Download groundtruth files

- You can download groundtruth files with this [link](https://www.robots.ox.ac.uk/~vgg/data/oxbuildings/gt_files_170407.tgz)

- Then you need to extract and put it in folder ```systems/datasets/```

```
systems
    └───datasets
            └───oxbuild_dataset
                    └───gt_files
                            │all_souls_1_good.txt
                            │all_souls_1_junk.txt
                            │all_souls_1_ok.txt
                            │all_souls_1_quey.txt
                            |...
```

## 3. Running Locally


### 3.1. Index dataset

For indexing dataset, please run the following command.

```bash
python3 systems/src/index_dataset.py
```

### 3.2. Evaluate system

For evaluate system, please run the following command.

```bash
python3 systems/src/evaluate_system.py.py
```

The resulting file will be saved at ```systems/datasets/```

```
systems
    └───datasets
            └───oxbuild_dataset
                    └───evaluation_result
                            │eval_result.txt
                            |...
```

### 3.3. Run the system on the web

In the first run, you need to run the following command.

```bash
python3 manage.py migrate
```

Then run the following command to start the system.

```bash
python3 manage.py runserver
```