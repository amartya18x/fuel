import os
import h5py

from scipy.io import loadmat

from fuel.converters.base import fill_hdf5_file, MissingInputFiles


def convert_silhouettes(size, directory, output_file):
    """ Convert the CalTech 101 Silhouettes Datasets.

    ToDo

    Parameters
    ----------
    size : int
        Either of 16 or 28
    directory : str
        Directory in which the required input files reside.
    output_file : str
        Where to save the converted dataset.

    """
    input_file = 'caltech101_silhouettes_{}_split1.mat'.format(size)
    input_file = os.path.join(directory, input_file)

    if not os.path.isfile(input_file):
        raise MissingInputFiles('Required files missing', [input_file])

    output_file = output_file.format(size)

    with h5py.File(output_file, mode="w") as h5file:
        mat = loadmat(input_file)

        train_X = mat['train_data'].reshape([-1, 1, size, size])
        valid_X = mat['val_data'].reshape([-1, 1, size, size])
        test_X  = mat['test_data'].reshape([-1, 1, size, size])
        train_Y = mat['train_labels']
        valid_Y = mat['val_labels']
        test_Y  = mat['test_labels']

        data = (
            ('train', 'features', train_X),
            ('train', 'targets' , train_Y),
            ('valid', 'features', valid_X),
            ('valid', 'targets' , valid_Y),
            ('test',  'features', test_X),
            ('test',  'targets' , test_Y),
        )
        fill_hdf5_file(h5file, data)

        for i, label in enumerate(('batch', 'channel', 'height', 'width')):
            h5file['features'].dims[i].label = label

        for i, label in enumerate(('batch', 'index')):
            h5file['targets'].dims[i].label = label


def fill_subparser(subparser):
    """Sets up a subparser to convert CalTech101 Silhouettes Database files.

    Parameters
    ----------
    subparser : :class:`argparse.ArgumentParser`
        Subparser handling the `caltech101_silhouettes` command.

    """
    subparser.add_argument(
        "size", type=int, choices=(16, 28),
        help="height/width of the datapoints")
    subparser.set_defaults(
        func=convert_silhouettes,
        output_file=os.path.join(os.getcwd(), 'caltech101_silhouettes{}.hdf5'))
