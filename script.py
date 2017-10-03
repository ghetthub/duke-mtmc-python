'''
'''

import os
import re
import urllib
import tarfile
import argparse


def get_default_params():
    params = {
        "cameras"    : [1, 2, 3, 4, 5, 6, 7, 8],
        "videoParts" : [9, 9, 9, 9, 9, 8, 8, 9],
        "data"       : {
            "ground_truth"         : [
                "trainval.mat",
                "trainvalRaw.mat"
            ],
            "calibration"      : [
                "calibration.txt",
                "camera_position.txt",
                "ROIs.txt"
            ],
            "detections" : {"camera*.mat" : ["cameras"]},
            "masks"      : {"camera*.tar.gz" : ["cameras"]},
            "videos"     : {"camera*/*.MTS" : ["cameras", "videoParts"]}
        },
    }

    return params


def read_json_file(json_file):
    with open(json_file) as f:
        params = json.loads(f)
        f.close()

    return params


def create_folder(dest, nbCams):
    folderNames = {'ground_truth', 'calibration', 'detections'}
    folderSubbedNames = {'frames', 'masks', 'videos'}

    for fName in folderNames:
        folderPath = os.path.join(dest, fName)
        if not os.path.isdir(folderPath):
            os.makedirs(folderPath)

    for fName in folderSubbedNames:
        for i in range(0, nbCams):
            camFolderName = "camera{}".format(i+1)
            folderPath = os.path.join(dest, fName, camFolderName)

            if not os.path.isdir(folderPath):
                os.makedirs(folderPath)


def extract_tar(fileName, verbose=False):
    if verbose: print("... Extracting {}".format(fileName))
    archivFile = tarfile.open(fileName)
    archivFile.extractall(os.path.join(source, 'masks'))
    archivFile.close()


def delete_tmp(fileName, verbose=False):
    if verbose: print("... Deleting {}".format(fileName))
    os.remove(fileName)


def download_from_list(dataType, data, dest, verbose=False):
    baseUrl = os.path.join('http://vision.cs.duke.edu/DukeMTMC/data', dataType)

    for value in data:
        fileName = os.path.join(dest, dataType, value)
        url = os.path.join(baseUrl, value)

        if verbose: print("..... Downloading {}".format(value))
        urllib.urlretrieve(url, fileName)


def download_from_dict(dataType, data, dest, params, verbose=False):
    baseUrl = os.path.join('http://vision.cs.duke.edu/DukeMTMC/data', dataType)

    for value in data:
        files = []

        for index in range(0, value.count('*')):
            if files == []:
                for elem in params[data[value][index]]:
                    newName = value.replace('*', str(elem), 1)
                    files.append(newName)
            else:
                newFiles = []
                for fileName in files:
                    for elem in params[data[value][index]]:
                        for i in range(0, elem):
                            newName = fileName.replace('*', str(i+1), 1)
                            newFiles.append(newName)
                files = newFiles


    for value in files:
        fileName = os.path.join(dest, dataType, value)
        url = os.path.join(baseUrl, value)

        if verbose: print("..... Downloading {}".format(value))
        urllib.urlretrieve(url, fileName)


def extract_video(dest, params):
    if dest == ".":
        dest = os.getcwd()

    for cam in range(0, len(params["cameras"])):
        fileName = os.path.join(dest, 'videos', 'camera{}'.format(cam+1))
        filelist = '"concat:00000.MTS';

        for k in range (0, params["videoParts"][cam]):
            filelist = '{}|0000{}.MTS'.format(filelist, k+1)

        # framesDir = os.path.join(dest, 'frames', 'camera{}'.format(cam+1), '%d.jpg')
        # command = 'ffmpeg -i {}" -qscale:v 1 -f image2 {}'.format(filelist, framesDir)

        framesDir = os.path.join(dest, 'frames', 'camera{}.mp4'.format(cam+1))
        command = 'ffmpeg -y -i {}" -qscale:v 1 -framerate 30 -vcodec libx264 {}'.format(filelist, framesDir)

        os.chdir(fileName)
        os.system(command)



def getDataset(dest='.', json=None, verbose=False):
    params = get_default_params()

    if not json == None:
        print("JSON given. Please do something!")

    if verbose: print("Patience, this may take 1-2 days!")

    # if verbose: print('Creating folder structure...')
    # create_folder(dest, len(params["cameras"]))
    #
    # if verbose: print("Downloading data...")
    # data = params["data"]
    # for key in data.keys():
    #     value = data[key]
    #     if not value == []:
    #         if verbose: print("... Downloading {}".format(key))
    #         if type(value) == list:
    #             download_from_list(key, value, dest, verbose)
    #
    #         if type(value) == dict:
    #             download_from_dict(key, value, dest, params, verbose)

    if verbose: print('Data download complete, now the extraction!')

    extract_video(dest, params)

    if verbose: print('Data extraction complete!')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Get dataset results')

    parser.add_argument(
        '-d',
        '--destination',
        type=str,
        default='.',
        help='destination path where to save the dataset')

    parser.add_argument(
        '-p',
        '--params',
        type=str,
        default=None,
        help='path to a JSON configuration file')

    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='activate verbose on the main function')

    args = parser.parse_args()

    getDataset(args.destination, args.params, args.verbose)
