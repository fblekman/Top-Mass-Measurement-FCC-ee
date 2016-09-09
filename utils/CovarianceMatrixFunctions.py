import numpy as np

def CombineCovarianceMatrices(covariance_matrix_list):
    """Combine two covariance matrices.

    The combination is done assuming that the fit parameters and the covariance
    matrices are obtained with a maximum likelihood fit, in the approximation of
    a gaussian likelihood (limit of big data sample): hence the combination is
    done as if you minimized a likelihood that is the product of the likelihoods
    of the single measurements.

    The argument must be a list of numpy 2-D array (shape n, n), and the result
    is a numpy 2-D array (shape n, n).
    """
    inverse_matrices = []
    for covariance_matrix in covariance_matrix_list:
        inverse_matrices.append( np.linalg.inv(covariance_matrix) )

    alpha = sum(inverse_matrices)
    inverse_alpha = np.linalg.inv(alpha)
    return inverse_alpha

def CombineFitParameters(fit_parameters_list, covariance_matrix_list):
    """Combine fit parameters from a list of measurements.

    The combination is done assuming that the fit parameters and the covariance
    matrices are obtained with a maximum likelihood fit, in the approximation of
    a gaussian likelihood (limit of big data sample): hence the combination is
    done as if you minimized a likelihood that is the product of the likelihoods
    of the single measurements.

    The arguments must be:
    fit_parameters_list: list of numpy 1-D array (shape 1, n)
    covariance_matrix_list: list of numpy 2-D array (shape n, n)

    The result is a numpy 1-D array (shape 1, n)
    """
    sum_fit_parameters = np.zeros_like(fit_parameters_list[0])
    for fit_parameters, covariance_matrix in zip(fit_parameters_list, covariance_matrix_list):
        aux_inv = np.linalg.inv(covariance_matrix)
        aux_fit_parameters = sum_fit_parameters + fit_parameters * aux_inv
        sum_fit_parameters = aux_fit_parameters
    combined_covariance_matrix = CombineCovarianceMatrices(covariance_matrix_list)
    combined_fit_parameters = sum_fit_parameters * combined_covariance_matrix
    return combined_fit_parameters

def RotateCovarianceMatrix(covariance_matrix, rotation_matrix):
    """Change variables of a covariance matrix.

    rotation_matrix is the matrix that, given the new variables, returns the old ones.
    The change of variables is done by applying the rotation_matrix to the inverse of the covariance_matrix in the following way: rot^T * cova^-1 * rot
    and then inverting again the result to obtain the new covariance matrix.

    The arguments must be:
    covariance_matrix: numpy 2-D array (shape n, n)
    rotation_matrix: numpy 2-D array (shape n, n)

    The result is a numpy 2-D array (shape n, n)
    """
    rotation_matrix_tr = np.transpose(rotation_matrix)
    second_der_matrix = np.linalg.inv(covariance_matrix)
    second_der_matrix_rotated = rotation_matrix_tr * second_der_matrix * rotation_matrix
    covariance_matrix_rotated = np.linalg.inv(second_der_matrix_rotated)
    return covariance_matrix_rotated
