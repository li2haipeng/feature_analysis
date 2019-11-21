from keras.models import Sequential, load_model
from keras.layers import Dense, Conv1D, MaxPooling1D, Dropout, GlobalAveragePooling1D, Flatten, BatchNormalization
from keras.models import Sequential
from keras.initializers import glorot_normal
from keras.callbacks import Callback, ModelCheckpoint, LearningRateScheduler, TensorBoard, EarlyStopping
import keras.backend as K
import sys
import numpy as np
import sys
sys.path.append('/home/lhp/PycharmProjects/feature_analysis')
import selfUtils as su
import pandas as pd


def default_params():
   return {
           'optimizer': 'Adamax',
           'learning_rate': 0.01,
           'activation1': 'tanh',
           'activation2': 'selu',
           'activation3': 'relu',
           'activation4': 'selu',
           'drop_rate1': 0.2,
           'drop_rate2': 0.5,
           'drop_rate3': 0.1,
           'drop_rate4': 0.2,
           'decay': 0.3254,
           'batch_size': 32,
           'epochs': 30,
           'data_dim': 2500,
           'conv1': 256,
           'conv2': 64,
           'conv3': 64,
           'conv4': 256,
           'pool1': 6,
           'pool2': 3,
           'pool3': 1,
           'pool4': 4,
           'kernel_size1': 14,
           'kernel_size2': 4,
           'kernel_size3': 4,
           'kernel_size4': 15,
           'dense1': 1024,
           'dense1_act': 'selu',
           }


def built_and_compile(params, num_classes):
    layers = [Conv1D(params['conv1'], kernel_size=params['kernel_size1'], activation=params['activation1'],
                     input_shape=(params['data_dim'], 1), use_bias=False, kernel_initializer=glorot_normal(seed=7)),
              BatchNormalization(),
              MaxPooling1D(params['pool1']),
              Dropout(rate=params['drop_rate1']),

              Conv1D(params['conv2'], kernel_size=params['kernel_size2'], activation=params['activation2'],
                     use_bias=False, kernel_initializer=glorot_normal(seed=7)),
              BatchNormalization(),
              MaxPooling1D(params['pool2']),
              Dropout(rate=params['drop_rate2']),

              Conv1D(params['conv3'], kernel_size=params['kernel_size3'], activation=params['activation3'],
                     use_bias=False, kernel_initializer=glorot_normal(seed=7)),
              BatchNormalization(),
              MaxPooling1D(params['pool3']),
              Dropout(rate=params['drop_rate3']),

              Conv1D(params['conv4'], kernel_size=params['kernel_size4'], activation=params['activation4'],
                     use_bias=False, kernel_initializer=glorot_normal(seed=7)),
              BatchNormalization(),
              MaxPooling1D(params['pool4']),
              GlobalAveragePooling1D(),

              Dense(params['dense1'], activation=params['dense1_act'], use_bias=False,
                    kernel_initializer=glorot_normal(seed=7)),
              BatchNormalization(),
              Dropout(rate=params['drop_rate4']),
              Dense(num_classes, activation='softmax', kernel_initializer=glorot_normal(seed=7))]

    model = Sequential(layers)
    model.compile(loss='categorical_crossentropy', optimizer=params['optimizer'], metrics=['accuracy'])

    return model


def test(params, X_test, y_test, NUM_CLASS):
    print ('Predicting results with best model...')
    model = built_and_compile(params, NUM_CLASS)
    model.load_weights('/home/lhp/PycharmProjects/dl_models/cnn_wf.hdf5')
    score, acc = model.evaluate(X_test, y_test, batch_size=100)
    print('Test score:', score)
    print('Test accuracy:', acc)


def main():
    # method = sys.argv[1]
    method = 'mrmr'
    model_path = '/home/lhp/PycharmProjects/dl_models/cnn_wf_padded.h5'
    model = load_model(model_path)
    # path = '/home/lhp/PycharmProjects/dataset/Alexa_dataset/numeric_class.csv'
    # selected_f = pd.read_csv(path,header=None)

    # selected_col = selected_f.iloc[:,0]
    # selected_col = sorted(selected_col)
    selected_col = [i for i in range(1, 3501)]
    X_train, y_train, X_test, y_test, num_classes = su.load_data('wf_padded_rr.csv', selected_col)

    # PARAMS = default_params()
    # test(PARAMS, X_test, y_test, num_classes)

    X_test = np.expand_dims(X_test, axis=2)
    score, acc = model.evaluate(X_test, y_test, batch_size=100)
    print(f"Model Performance: {score, acc}")


if __name__ == '__main__':
    main()