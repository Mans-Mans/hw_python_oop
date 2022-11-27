LEN_STEP = 0.65
M_IN_KM = 1000
CALORIES_MEAN_SPEED_MULTIPLIER = 18
CALORIES_MEAN_SPEED_SHIFT = 1.79
CALORIES_WEIGHT_MULTIPLIER = 0.035
CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
CALORIES_AVARAGE_SPEED_MULTIPLIER = 1.1
CALORIES_WEIGHT_DURATION_MULTIPLIER = 2
KMH_IN_MSEC = 0.278
MIN_IN_H = 60
CM_IN_M = 100


class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> str:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type:}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.'
                )


class Training:
    """Базовый класс тренировки."""
    MIN_IN_H = 60
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> str:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * LEN_STEP / M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return (InfoMessage(type(self).__name__,
                self.duration,
                self.get_distance(),
                self.get_mean_speed(),
                self.get_spent_calories())
                )


class Running(Training):
    """Тренировка: бег."""
    LEN_STEP = 0.65
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        """Подсчет израсходованных калорий при беге."""
        run_calories = ((CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                        + CALORIES_MEAN_SPEED_SHIFT) * self.weight / M_IN_KM
                        * self.duration * MIN_IN_H)
        return run_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    LEN_STEP = 0.65
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100
    MIN_IN_H = 60

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Подсчет израсходованных калорий при спортивной ходьбе."""
        avarage_speed_IN_MSEC = self.get_mean_speed() * KMH_IN_MSEC
        walk_calories = ((CALORIES_WEIGHT_MULTIPLIER * self.weight
                         + (avarage_speed_IN_MSEC**2 / (self.height / CM_IN_M))
                         * CALORIES_SPEED_HEIGHT_MULTIPLIER
                         * self.weight) * self.duration * MIN_IN_H)
        return walk_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    CALORIES_AVARAGE_SPEED_MULTIPLIER = 1.1
    CALORIES_WEIGHT_DURATION_MULTIPLIER = 2
    M_IN_KM = 1000

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        LEN_STEP = 1.38
        return self.action * LEN_STEP / M_IN_KM

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Вычисление средней скорости при плавании."""
        mean_speed = (self.length_pool * self.count_pool
                      / M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Подсчет израсходованных калорий при плавании."""
        spent_calories = ((self.get_mean_speed()
                          + CALORIES_AVARAGE_SPEED_MULTIPLIER)
                          * CALORIES_WEIGHT_DURATION_MULTIPLIER
                          * self.weight * self.duration)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    commands = {'SWM': Swimming,
                'RUN': Running,
                'WLK': SportsWalking
                }
    if workout_type in commands:
        training_class: Training = commands[workout_type](*data)
        return training_class


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
