import copy


class Matrix:
    def __init__(self, values, n=0, m=0):
        self.values = values
        self.n = n if n != 0 else len(values)
        self.m = m if m != 0 else len(values[0])

    def __repr__(self):
        out = ''
        for row in self.values:
            out += ' '.join(map(str, row)) + '\n'
        return out

    def add_matrix(self, matrix):
        if (self.n != matrix.n) or (self.m != matrix.m):
            raise MatrixProcessorException()

        out = []
        for i in range(self.n):
            row = []
            for j in range(self.m):
                row.append(self.values[i][j] + matrix.values[i][j])
            out.append(row)
        return Matrix(out, self.n, self.m)

    def multiply_by_num(self, num):
        out = [[elem * num for elem in row] for row in self.values]
        return Matrix(out, self.n, self.m)

    def multiply_by_matrix(self, matrix):
        if self.m != matrix.n:
            raise MatrixProcessorException()

        out = []
        for row in self.values:
            out_row = []
            for i in range(matrix.m):
                column = []
                for j in range(matrix.n):
                    column.append(matrix.values[j][i])
                elem = sum([row[j] * column[j] for j in range(self.m)])
                out_row.append(elem)
            out.append(out_row)
        return Matrix(out, self.m, self.m)

    def transpose_main(self):
        out = []
        for j in range(self.m):
            row = []
            for i in range(self.n):
                row.append(self.values[i][j])
            out.append(row)
        return Matrix(out, self.m, self.n)

    def transpose_side(self):
        out = []
        for j in range(self.m):
            row = []
            for i in range(self.n):
                row.append(self.values[-i - 1][-j - 1])
            out.append(row)
        return Matrix(out, self.m, self.n)

    def transpose_vertical(self):
        out = [row[::-1] for row in self.values]
        return Matrix(out, self.n, self.m)

    def transpose_horizontal(self):
        out = [self.values[-i - 1] for i in range(self.n)]
        return Matrix(out, self.n, self.m)

    def get_minor(self, i, j):
        sub_values = copy.deepcopy(self.values)
        for x in range(self.n):
            del sub_values[x][j]
        del sub_values[i]
        sub_matrix = Matrix(sub_values, self.n - 1, self.m - 1)
        return sub_matrix.get_determinant()

    def get_cofactor_value(self, i, j):
        return (-1) ** (i + j) * self.get_minor(i, j)

    def get_determinant(self):
        if self.n != self.m:
            raise MatrixProcessorException()

        if self.n == 1:
            return self.values[0][0]

        if self.n == 2:
            return self.values[0][0] * self.values[1][1] - self.values[0][1] * self.values[1][0]

        if self.n > 2:
            det = 0
            for j in range(self.m):
                det += self.values[0][j] * self.get_cofactor_value(0, j)
            return det

    def get_cofactor_matrix(self):
        out = []
        for i in range(self.n):
            row = []
            for j in range(self.m):
                row.append(self.get_cofactor_value(i, j))
            out.append(row)
        return Matrix(out, self.n, self.m)

    def get_inverse_matrix(self):
        det = self.get_determinant()
        if det == 0:
            raise MatrixProcessorException("This matrix doesn't have an inverse.")
        cof_matrix = self.get_cofactor_matrix().transpose_main()
        return cof_matrix.multiply_by_num(1 / det)


class MatrixProcessorException(Exception):
    def __init__(self, msg='The operation cannot be performed.', *args):
        super(MatrixProcessorException, self).__init__(msg, *args)


def read_matrix(number=''):
    if number != '':
        number += ' '
    n, m = map(int, input(f'Enter size of {number}matrix: ').split())
    print(f'Enter {number}matrix:')
    rows = []
    for i in range(n):
        row = list(map(float, input().split()))
        rows.append(row)
    return Matrix(rows, n, m)


def main():
    while True:
        choice = int(input('1. Add matrices\n'
                           '2. Multiply matrix by a constant\n'
                           '3. Multiply matrices\n'
                           '4. Transpose matrix\n'
                           '5. Calculate a determinant\n'
                           '6. Inverse matrix\n'
                           '0. Exit\n'
                           'Your choice: '))

        if choice == 0:
            break

        if choice == 1:
            matrix_a = read_matrix('first')
            matrix_b = read_matrix('second')
            try:
                result_matrix = matrix_a.add_matrix(matrix_b)
                print(f'The result is:\n{result_matrix}')
            except MatrixProcessorException as e:
                print(e)

        if choice == 2:
            matrix = read_matrix()
            num = float(input('Enter constant: '))
            result_matrix = matrix.multiply_by_num(num)
            print(f'The result is:\n{result_matrix}')

        if choice == 3:
            matrix_a = read_matrix('first')
            matrix_b = read_matrix('second')
            try:
                result_matrix = matrix_a.multiply_by_matrix(matrix_b)
                print(f'The result is:\n{result_matrix}')
            except MatrixProcessorException as e:
                print(e)

        if choice == 4:
            transpose_choice = int(input('1. Main diagonal\n'
                                         '2. Side diagonal\n'
                                         '3. Vertical line\n'
                                         '4. Horizontal line\n'
                                         'Your choice: '))
            matrix = read_matrix()
            result_matrix = None
            if transpose_choice == 1:
                result_matrix = matrix.transpose_main()
            if transpose_choice == 2:
                result_matrix = matrix.transpose_side()
            if transpose_choice == 3:
                result_matrix = matrix.transpose_vertical()
            if transpose_choice == 4:
                result_matrix = matrix.transpose_horizontal()
            print(f'The result is:\n{result_matrix}')

        if choice == 5:
            matrix = read_matrix()
            try:
                result = matrix.get_determinant()
                print(f'The result is:\n{result}')
            except MatrixProcessorException as e:
                print(e)

        if choice == 6:
            matrix = read_matrix()
            try:
                result_matrix = matrix.get_inverse_matrix()
                print(f'The result is:\n{result_matrix}')
            except MatrixProcessorException as e:
                print(e)


if __name__ == '__main__':
    main()
