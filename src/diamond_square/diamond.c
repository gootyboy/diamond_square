#include <stdio.h>
#include <stdlib.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    size_t rows;
    size_t cols;
    double **data;
} Array2D;

double random_custom() {
    return rand() / (double) RAND_MAX;
}

double random_uniform(double min, double max) {
    if (min > max) {
        double temp = min;
        min = max;
        max = temp;
    }

    double scale = random_custom();
    return min + scale * (max - min);
}

Array2D create_array2d(size_t rows, size_t cols) {
    Array2D array2d;
    array2d.rows = rows;
    array2d.cols = cols;
    array2d.data = malloc(array2d.rows * sizeof(double*));

    if (array2d.data == NULL) {
        printf("Malloc failed for rows.\n");
        exit(EXIT_FAILURE);
    }

    for (size_t i = 0; i < rows; i++) {
        array2d.data[i] = malloc(array2d.cols * sizeof(double));
        if (array2d.data[i] == NULL) {
            printf("Malloc failed for row %zu.\n", i);
            for (size_t j = 0; j < i; j++) {
                free(array2d.data[j]);
            }
            free(array2d.data);
            exit(EXIT_FAILURE);
        }
    }

    return array2d;
}

void free_array2d(Array2D array2d) {
    for (size_t i = 0; i < array2d.rows; i++) {
        free(array2d.data[i]);
    }

    free(array2d.data);
}

double** diamond_square(int size, float rough) {
    Array2D h_map = create_array2d(size, size);

    for (int y = 0; y < size; y++)
        for (int x = 0; x < size; x++)
            h_map.data[y][x] = 0.0;

    h_map.data[0][0] = random_custom();
    h_map.data[0][size - 1] = random_custom();
    h_map.data[size - 1][0] = random_custom();
    h_map.data[size - 1][size - 1] = random_custom();

    int step = size - 1;
    float s = rough;

    while (step > 1) {
        int half = step / 2;

        for (int y = half; y < size - 1; y += step) {
            for (int x = half; x < size - 1; x += step) {
                double avg =
                    (h_map.data[y-half][x-half] +
                     h_map.data[y-half][x+half] +
                     h_map.data[y+half][x-half] +
                     h_map.data[y+half][x+half]) / 4.0;

                h_map.data[y][x] = avg + random_uniform(-s, s);
            }
        }

        for (int y = 0; y < size; y += half) {
            for (int x = ((y + half) % step); x < size; x += step) {
                double total = 0;
                int count = 0;

                int dirs[4][2] = {
                    {-half, 0}, {half, 0},
                    {0, -half}, {0, half}
                };

                for (int i = 0; i < 4; i++) {
                    int ny = y + dirs[i][0];
                    int nx = x + dirs[i][1];
                    if (ny >= 0 && ny < size && nx >= 0 && nx < size) {
                        total += h_map.data[ny][nx];
                        count++;
                    }
                }

                h_map.data[y][x] = (total / count) + random_uniform(-s, s);
            }
        }

        step /= 2;
        s *= rough;
    }

    double minv = h_map.data[0][0];
    double maxv = h_map.data[0][0];

    for (int y = 0; y < size; y++)
        for (int x = 0; x < size; x++) {
            if (h_map.data[y][x] < minv) minv = h_map.data[y][x];
            if (h_map.data[y][x] > maxv) maxv = h_map.data[y][x];
        }

    double range = maxv - minv + 0.0001;
    for (int y = 0; y < size; y++)
        for (int x = 0; x < size; x++)
            h_map.data[y][x] = (h_map.data[y][x] - minv) / range;

    return h_map.data;
}

#ifdef __cplusplus
}
#endif
