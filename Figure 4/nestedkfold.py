import pandas as pd
import numpy as np
from sklearn import datasets, linear_model, svm
from sklearn.metrics import mean_absolute_error, r2_score, mean_absolute_error
from sklearn.utils import shuffle
from sklearn.model_selection import KFold
from matplotlib import pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

for round in range(3):
    #load dataset
    data = pd.read_csv("users_data_regression.csv")
    data = shuffle(data)#,random_state=0)
    data.reset_index(inplace=True, drop=True)
    df1 = data[['Average of vmaf', 'Var of vmaf', 'Sum of rebuffering_duration']]

    #define cv split
    cv = KFold(n_splits=5, random_state=18 ,shuffle=False) #random_state produce lo stesso random 18 reg

    # take data for mos hyper cv from loaded dataset
    data_X = df1.to_numpy()
    mos = data['mos']
    data_y_m = mos.to_numpy()

    #cross validation hyperpar mos
    mantainparfoldmos=[]
    for train_index, valid_index in cv.split(data_X):
        X_train_mos, X_valid_mos, y_train_mos, y_val_mos = data_X[train_index], data_X[valid_index],data_y_m[train_index], data_y_m[valid_index]
        # gridsearch for hyperpar
        parammos = []
        kernels = ['rbf', 'sigmoid', 'poly']
        Cpar = [1, 10, 15, 20, 30, 50, 60, 100]
        mesh = np.array(np.meshgrid(kernels, Cpar))
        combinationspar = mesh.T.reshape(-1, 2)
        for ker in kernels:
            for c in Cpar:
                # create non linear svr model
                usrmos = make_pipeline(StandardScaler(), svm.SVR(kernel=ker, C=c, epsilon=0.1))

                # train and predict for user in validation
                svrmodelmos = usrmos.fit(X_train_mos, y_train_mos)
                data_y_pred_mos_svr = svrmodelmos.predict(X_valid_mos)
                mossvrmse = mean_absolute_error(y_val_mos, data_y_pred_mos_svr)
                parammos.append(mossvrmse)
        mantainparfoldmos.append(parammos)

    #select best hyper parameter after cv save it into kmos cmos
    mantainavemos=np.mean(mantainparfoldmos,axis=0)
    mantainparfoldmos=[]
    index_best_par_mos = mantainavemos.argmin()
    kmos, cmos = combinationspar[index_best_par_mos]
    cmos = int(cmos)
    print('mosbestparmos {}{}'.format(kmos,cmos))

    #array for final results
    finaldiff=[]
    usrerr=[]
    usrvar=[]
    moserr=[]
    mosvar=[]

    finaldifflin = []
    usrerrlin = []
    usrvarlin = []
    moserrlin = []
    mosvarlin = []


    #loop for each user
    for i in range(8,40):
        data_X = df1.to_numpy()
        mos = data['mos']
        data_y_m = mos.to_numpy()
        user = data.iloc[:, i]
        data_y_u = user.to_numpy()

        # dati per stratificare
        #bins = np.linspace(0, 449, 45)
        #y_u_binned = np.digitize(data_y_u, bins)
        #y_u_binned,data_X_clean,data_y_u=remove_out_val(y_u_binned,data_X,data_y_u)

        # array for save each user result
        arrsvrmos = []
        arrsvrusr = []
        arrlinusr = []
        arrlinmos = []
        diffusereachfold = []
        contafoldext=0

        #cross validation esterna
        for train_val_index, test_index in cv.split(data_X):
            X_trainval_usr, X_test_usr, y_trainval_usr, y_test_usr = data_X[train_val_index],data_X[test_index],data_y_u[train_val_index],data_y_u[test_index]
            contafoldext += 1
            mantainparfold=[]

            #cross validation internal user
            contafoldint = 0
            for train_index, valid_index in cv.split(X_trainval_usr):
                X_train_usr, X_valid_usr, y_train_u, y_val_u = X_trainval_usr[train_index], X_trainval_usr[valid_index],y_trainval_usr[train_index], y_trainval_usr[valid_index]
                contafoldint = contafoldint + 1

                # gridsearch for hyperpar
                paramusr = []
                kernels = ['rbf', 'sigmoid', 'poly']
                Cpar = [1, 10, 15, 20, 30, 50, 60, 100]
                mesh = np.array(np.meshgrid(kernels, Cpar))
                combinationspar = mesh.T.reshape(-1, 2)
                for ker in kernels:
                    for c in Cpar:
                        # create non linear svr model
                        usrsvr = make_pipeline(StandardScaler(), svm.SVR(kernel=ker, C=c, epsilon=0.1))

                        # train and predict for user in validation
                        svrmodelus = usrsvr.fit(X_train_usr, y_train_u)
                        data_y_pred_u_svr = svrmodelus.predict(X_valid_usr)
                        usrsvrmse = mean_absolute_error(y_val_u, data_y_pred_u_svr)
                        paramusr.append(usrsvrmse)
                mantainparfold.append(paramusr)
                print('inner fold: {}'.format(contafoldint))

            # find best one in all media delle cv interne
            mantainaveusr = np.mean(mantainparfold, axis=0)
            mantainparfoldusr = []
            index_best_par_usr = mantainaveusr.argmin()
            kusr, cusr = combinationspar[index_best_par_usr]
            cusr = int(cusr)
            print('user {}, extfold {} ,  inter cv finished, usrbestparus {}{}'.format(i,contafoldext,kusr, cusr))

            # train fold esterne
            # define model with hyper find in internal cv
            usrsvr = make_pipeline(StandardScaler(), svm.SVR(kernel=kusr, C=cusr, epsilon=0.1))
            mossvr = make_pipeline(StandardScaler(), svm.SVR(kernel=kmos, C=cmos, epsilon=0.1))

            # linear model without hyperpar
            usrlin=linear_model.LinearRegression()
            moslin=linear_model.LinearRegression()

            #usr
            #svr
            svrmodelus = usrsvr.fit(X_trainval_usr, y_trainval_usr)
            data_y_pred_u_svr = svrmodelus.predict(X_test_usr)
            usrsvrmse = mean_absolute_error(y_test_usr, data_y_pred_u_svr)
            arrsvrusr.append(usrsvrmse)
            #lin (wrapped into a try except beacause from time to time it gives error of convergence that seems to be fixed by reinitialize the variable)
            try:
                usrlin.fit(X_trainval_usr, y_trainval_usr)
            except:
                usrlin = linear_model.LinearRegression()
                usrlin.fit(X_trainval_usr, y_trainval_usr)
            data_y_pred_u_lin = usrlin.predict(X_test_usr)
            usrlinmse = mean_absolute_error(y_test_usr, data_y_pred_u_lin)
            arrlinusr.append(usrlinmse)

            #mos
            #svr
            svrmodelus = usrsvr.fit(data_X, data_y_m)
            data_y_pred_mos_svr = svrmodelus.predict(X_test_usr)
            mossvrmse = mean_absolute_error(y_test_usr, data_y_pred_mos_svr)
            arrsvrmos.append(mossvrmse)
            # lin
            moslin.fit(data_X, data_y_m)
            data_y_pred_mos_lin = moslin.predict(X_test_usr)
            moslinmse = mean_absolute_error(y_test_usr, data_y_pred_mos_lin)
            arrlinmos.append(moslinmse)

        #save result for each user and at the end of all out fold
        #svr
        usrerr.append(np.average(arrsvrusr))
        usrvar.append(np.std(arrsvrusr))
        moserr.append(np.average(arrsvrmos))
        mosvar.append(np.std(arrsvrmos))
        finaldiff.append(np.average(arrsvrmos) - np.average(arrsvrusr))
        #lin
        usrerrlin.append(np.average(arrlinusr))
        usrvarlin.append(np.std(arrlinusr))
        moserrlin.append(np.average(arrlinmos))
        mosvarlin.append(np.std(arrlinmos))
        finaldifflin.append(np.average(arrlinmos) - np.average(arrlinusr))


    #ordina utenti secondo condizione e plotta
    hdtvordereduser=[26,8,22,31,12,16,28,11,7,30,24,10,21,5,13,15,18,2,4,3,9,17,14,23,25,20,27,19,6,32,1,29]
    sorteddiff=[]
    sorteddmosave=[]
    sorteddmosstd=[]
    sorteddusrave=[]
    sorteddusrstd=[]

    sorteddifflin=[]
    sorteddmosavelin=[]
    sorteddmosstdlin=[]
    sorteddusravelin=[]
    sorteddusrstdlin=[]
    for i in hdtvordereduser:
        sorteddiff.append(finaldiff[i-1])
        sorteddmosave.append(moserr[i-1])
        sorteddmosstd.append(mosvar[i-1])
        sorteddusrave.append(usrerr[i-1])
        sorteddusrstd.append(usrvar[i-1])

        sorteddifflin.append(finaldifflin[i - 1])
        sorteddmosavelin.append(moserrlin[i - 1])
        sorteddmosstdlin.append(mosvarlin[i - 1])
        sorteddusravelin.append(usrerrlin[i - 1])
        sorteddusrstdlin.append(usrvarlin[i - 1])

    fig1, ax1 = plt.subplots()
    us=[]
    for i in hdtvordereduser:
        us.append("u"+str(i))
    _X = np.arange(len(us))
    ax1.bar(_X - 0.2,sorteddifflin,yerr=np.array(sorteddmosstdlin)+np.array(sorteddusrstdlin), color='b', width=0.4)
    ax1.bar(_X + 0.2,sorteddiff,yerr=np.array(sorteddmosstd)+np.array(sorteddusrstd),color='r',width=0.4)
    plt.xticks(_X, us) # set labels manually
    plt.show()
    plt.savefig('fig'+str(round)+'.png')

    fig2, ax2 = plt.subplots()
    us=[]
    for i in hdtvordereduser:
        us.append("user "+str(i))
    _X = np.arange(len(us))
    plt.bar(_X+0.2, sorteddmosave,yerr=sorteddmosstd,color='r',width=0.4)
    plt.bar(_X-0.2,sorteddmosavelin,yerr=sorteddmosstdlin,color='b',width=0.4)
    plt.xticks(_X, us)
    #plt.show()

    fig3, ax3 = plt.subplots()
    us=[]
    for i in hdtvordereduser:
        us.append("user "+str(i))
    _X = np.arange(len(us))
    ax3.bar(_X+0.2, sorteddusrave,yerr=sorteddusrstd,color='r',width=0.4)
    ax3.bar(_X-0.2, sorteddusravelin,yerr=sorteddusrstdlin,color='b',width=0.4)
    plt.xticks(_X, us)
    #plt.show()


    # # save log date for each round
    # contalista=0
    # for selectedlist in [sorteddiff,sorteddifflin,sorteddmosave,sorteddmosstd,sorteddmosavelin,sorteddmosstdlin,sorteddusrave,sorteddusrstd,sorteddusravelin,sorteddusrstdlin]:
    #     with open(str(round)+'result list'+str(contalista)+'.txt', 'w') as f:
    #         for item in selectedlist:
    #             f.write("%s\n" % item)
    #     contalista = contalista + 1

