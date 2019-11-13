from keras.models import Sequential, load_model
import numpy as np
import sys
sys.path.append('/home/lhp/PycharmProjects/feature_analysis')
import selfUtils as su


def permutation(X, y_test):
    model_path = '/home/lhp/PycharmProjects/dl_models/cnn.h5'
    model = load_model(model_path)
    col_num = X.shape[1]
    step = 10
    iterations = int(400/step)
    for i in range(iterations):
        feature_set=[j for j in range(i, i+step)]
        X_p = X.copy()
        col = X.iloc[:,feature_set].sample(frac=1)
        col = col.sample(frac=1,axis=1)
        # X_p[str(i+1)] = list(col)
        X_p.iloc[:,feature_set] = (col).values
        X_test = np.expand_dims(X_p, axis=2)
        score, acc = model.evaluate(X_test, y_test, batch_size=100)
        print(f"Model Performance: {score, acc} at feature {feature_set}")


def main():
    selected_col = [i for i in range(1, 401)]
    X_train, y_train, X_test, y_test, num_classes = su.load_data('/home/lhp/PycharmProjects/dataset/Alexa_dataset/generic_class.csv', selected_col)
    permutation(X_test, y_test)




if __name__ == '__main__':
    main()