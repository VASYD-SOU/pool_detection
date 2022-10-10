# import the necessary packages
import os

# define the base path to the *original* input dataset and then use
# the base path to derive the image and annotations directories
ORIG_BASE_PATH = r'P:\Workspace\pool_detection\swimmingPool\training'
ORIG_IMAGES = os.path.sep.join([ORIG_BASE_PATH, 'images'])
ORIG_ANNOTS = os.path.sep.join([ORIG_BASE_PATH, 'labels'])

# define the base path to the *new* dataset after running our dataset
# builder scripts and then use the base path to derive the paths to
# our output class label directories
BASE_PATH = r'P:\Workspace\pool_detection\dataset'
POSITVE_PATH = os.path.sep.join([BASE_PATH, 'pool'])
NEGATIVE_PATH = os.path.sep.join([BASE_PATH, 'no_pool'])

# define the number of max proposals used when running selective
# search for (1) gathering training data and (2) performing inference
MAX_PROPOSALS = 10000
MAX_PROPOSALS_INFER = 500

# define the maximum number of positive and negative images to be
# generated from each image
MAX_POSITIVE = 10
MAX_NEGATIVE = 1

# initialize the input dimensions to the network
INPUT_DIMS = (224, 224)

# define the path to the output model and label binarizer
#MODEL_PATH = r'P:\Workspace\pool_detection\pool_detectionpool_detector_nr1.h5'
MODEL_PATH = r'P:\Workspace\pool_detection\pool_detectionpool_detector_nr2.h5' # Best so far!

# ANVÄND DENNA NÄR DU TRÄNAR NÄTVERKET!!!
#****************************
#MODEL_PATH = r'P:\Workspace\pool_detection\pool_detectionpool_detector.h5'
#****************************

ENCODER_PATH = r'P:\Workspace\pool_detection\pool_detectionlabel_encoder.pickle'

# define the minimum probability required for a positive prediction
# (used to filter out false-positive predictions)
MIN_PROBA = 0.75

# define the overlap threshhold for nms
NMS_OVERLAP_THRESH = 0.3