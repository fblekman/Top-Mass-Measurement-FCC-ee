import numpy as np

def CombineCovarianceMatrices(covariance_matrix_list):
    """Combine two covariance matrices.

    The arguments must be numpy 2-D array.
    """
    inverse_matrices = []
    for covariance_matrix in covariance_matrix_list:
        inverse_matrices.append( np.linalg.inv(covariance_matrix) )

    alpha = sum(inverse_matrices)
    inverse_alpha = np.linalg.inv(alpha)
    return inverse_alpha

def RotateCovarianceMatrix(covariance_matrix, rotation_matrix):
    rotation_matrix_tr = np.transpose(rotation_matrix)
    second_der_matrix = np.linalg.inv(covariance_matrix)
    second_der_matrix_rotated = rotation_matrix_tr * second_der_matrix * rotation_matrix
    covariance_matrix_rotated = np.linalg.inv(second_der_matrix_rotated)
    return covariance_matrix_rotated
