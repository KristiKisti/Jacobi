import numpy as np
from numpy import zeros
from flask import Flask, Response, request, jsonify, render_template

app = Flask(__name__)

def Jacobi(A, B):

    n=5
    X  = np.zeros((1, n))
    eps=0.001
    tmpX= np.zeros((1, n))
    max=10000
    for i in range(n):
        tmpX[0][i]=0
    norma=0
    for j in range(n):
        norma=norma+abs(A[0,j])
    for i in range(n):
        sum=0
        for j in range(n):
            sum+=abs(A[i,j])
        if sum>norma:
            norma=sum
    norma=eps*(1-norma)/norma
    while max>=abs(norma):
        for i in range(n):
            sum=0
            for j in range(n):
                if i!=j:
                    sum+=A[i,j]*tmpX[0][j]
            X[0][i]=1/A[i,i]*(B[i]-sum)
        max=abs(tmpX[0][0]-X[0][0])
        for j in range(n):
            if abs(tmpX[0][j]-X[0][j])>max:
                max=abs(tmpX[0][j]-X[0][j])
        for i in range(n):
            tmpX[0][i]=X[0][i]
    return [X[0]]

@app.route("/")
def client():
    return render_template("client.html")


@app.route("/Process", methods=['POST'])
def Process():
    system = request.json
    A = np.asarray(system['A'], dtype=float)
    B = np.asarray(system['B'], dtype=float)

    for i in range(5):
            sum=0
            for j in range(5):
                sum=sum+abs(A[i,j])
            if abs(A[i,i])<abs(sum-A[i,i]):
                return Response("{\"message\":\" Невозможно решить методом Якоби.\"}", status=404)
    result = Jacobi(A, B)
    return jsonify({"result": list(result[0])})

if __name__ == '__main__':
    app.run(debug=True)



