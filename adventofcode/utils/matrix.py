def transpose(matrix):
    """Transposes a 2D array
    """
    transposed = [
        [
            matrix[j][i]
            for j
            in range(len(matrix))
        ]
        for i
        in range(len(matrix[0]))
    ]
    return transposed
