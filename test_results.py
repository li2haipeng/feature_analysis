from keras.models import Sequential, load_model
import numpy as np
import sys
sys.path.append('/home/lhp/PycharmProjects/feature_analysis')
import selfUtils as su
import pandas as pd


def main():
    # method = sys.argv[1]
    method = 'mrmr'
    model_path = '/home/lhp/PycharmProjects/dl_models/cnn_video_bin.h5'
    model = load_model(model_path)
    # path = '/home/lhp/PycharmProjects/dataset/Alexa_dataset/numeric_class.csv'
    # selected_f = pd.read_csv(path,header=None)

    # selected_col = selected_f.iloc[:,0]
    # selected_col = sorted(selected_col)
    selected_col = [i for i in range(1, 721)]
    X_train, y_train, X_test, y_test, num_classes = su.load_data('/home/lhp/PycharmProjects/feature_analysis/video_bin_dp_5e-6_30.csv', selected_col)
    X_test = np.expand_dims(X_test, axis=2)
    score, acc = model.evaluate(X_test, y_test, batch_size=100)
    print(f"Model Performance: {score, acc}")


if __name__ == '__main__':
    main()