from typing import Type
from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        message = ('Тип тренировки: {training_type}; '
                   'Длительность: {duration:.3f} ч.; '
                   'Дистанция: {distance:.3f} км; '
                   'Ср. скорость: {speed:.3f} км/ч; '
                   'Потрачено ккал: {calories:.3f}.')
        return message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    MIN_IN_H: float = 60.0
    KMH_IN_MSEC: float = 0.278
    M_IN_KM: float = 1000.0
    CM_IN_M: float = 100.0
    LEN_STEP: float = 0.65

    def __init__(self,
                 action: float,
                 duration: float,
                 weight: float,
                 ) -> str:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите get_spent calories в '
                                  'class ' + type(self).__name__)

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
    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18.0
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Подсчет израсходованных калорий при беге."""
        run_calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                        * self.get_mean_speed()
                        + self.CALORIES_MEAN_SPEED_SHIFT)
                        * self.weight / self.M_IN_KM
                        * self.duration * self.MIN_IN_H)
        return run_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029

    def __init__(self, action: float,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Подсчет израсходованных калорий при спортивной ходьбе."""
        avarage_speed_IN_MSEC = self.get_mean_speed() * self.KMH_IN_MSEC
        walk_calories = ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                         + (avarage_speed_IN_MSEC**2
                          / (self.height / self.CM_IN_M))
                         * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                         * self.weight) * self.duration * self.MIN_IN_H)
        return walk_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_AVARAGE_SPEED_MULTIPLIER: float = 1.1
    CALORIES_WEIGHT_DURATION_MULTIPLIER: float = 2.0

    def __init__(self, action: float,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Вычисление средней скорости при плавании."""
        mean_speed = (self.length_pool * self.count_pool
                      / self.M_IN_KM / self.duration)
        return mean_speed

    def get_spent_calories(self) -> float:
        """Подсчет израсходованных калорий при плавании."""
        spent_calories = ((self.get_mean_speed()
                          + self.CALORIES_AVARAGE_SPEED_MULTIPLIER)
                          * self.CALORIES_WEIGHT_DURATION_MULTIPLIER
                          * self.weight * self.duration)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    commands: dict[str, Type[Training]] = {'SWM': Swimming,
                                           'RUN': Running,
                                           'WLK': SportsWalking
                                           }
    if workout_type in commands:
        return commands[workout_type](*data)
    else:
        raise TypeError(f'Введенная вами тренировка "{workout_type}" '
                        f'не распознана. Датчики принимают только '
                        f'следющие значения: '
                        f'{"; ".join(list(commands.keys()))}.')


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
