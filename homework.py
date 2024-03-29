from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str  # вид тренировки
    duration: float  # длительность тренировки, ч
    distance: float  # пройденная за тренировку дистанция, м
    speed: float  # скорость атлета, км/ч
    calories: float  # потраченные атлетом килокалории, шт

    def get_message(self) -> str:
        """Округлить и подготовить данные для вывода в сообщение."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.'
                )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65  # длина 1 шага в метрах
    M_IN_KM: int = 1000  # метров в 1 км
    MIN_IN_HOUR: int = 60  # минут в 1 часе

    def __init__(self,
                 action: int,  # количество движений, шт
                 duration: float,  # длительность тренировки, ч
                 weight: float  # вес атлета, кг
                 ) -> None:
        self.action: int = action
        self.duration: float = duration
        self.weight: float = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        result = (self.action * self.LEN_STEP / self.M_IN_KM)
        return result

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        result = (self.get_distance() / self.duration)
        return result

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError()

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        display_data = InfoMessage(self.__class__.__name__, self.duration,
                                   self.get_distance(), self.get_mean_speed(),
                                   self.get_spent_calories())
        return display_data


class Running(Training):
    """Тренировка: бег."""

    COEFF_CALORIE_RUN_1: int = 18  # коэф. No1 для калорий бега
    COEFF_CALORIE_RUN_2: int = 20  # коэф. No2 для калорий бега

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для бега."""
        training_time = self.duration * self.MIN_IN_HOUR
        result = (((self.COEFF_CALORIE_RUN_1 * self.get_mean_speed()
                  - self.COEFF_CALORIE_RUN_2)
                  * self.weight) / self.M_IN_KM * training_time)
        return result


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    COEFF_CALORIE_SPWLK_1: float = 0.035  # коэф. No1 для калорий ходьбы
    COEFF_CALORIE_SPWLK_2: float = 0.029  # коэф. No2 для калорий ходьбы

    def __init__(self,
                 action: int,  # количество движений, шт
                 duration: float,  # длительность тренировки, ч
                 weight: float,  # вес атлета, кг
                 height: float  # рост атлета, см
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height: float = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для спортивной ходьбы."""
        training_time = self.duration * self.MIN_IN_HOUR
        result = ((self.COEFF_CALORIE_SPWLK_1 * self.weight
                  + ((self.get_mean_speed() ** 2) // self.height)
                  * self.COEFF_CALORIE_SPWLK_2 * self.height) * training_time)
        return result


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38  # преодолеваемое расстояние за один гребок
    COEFF_CALORIE_SWIM_1: float = 1.1  # коэф. No1 для калорий плавания
    COEFF_CALORIE_SWIM_2: float = 2  # коэф. No1 для калорий плавания

    def __init__(self,
                 action: int,  # количество движений, шт
                 duration: float,  # длительность тренировки, ч
                 weight: float,  # вес атлета, кг
                 length_pool: float,  # длина бассейна, м
                 count_pool: int  # количество бассейнов за тренировку, шт
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool: float = length_pool
        self.count_pool: int = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения для плавания."""
        result = ((self.length_pool * self.count_pool)
                  / self.M_IN_KM / self.duration)
        return result

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для плавания."""
        result = ((self.get_mean_speed() + self.COEFF_CALORIE_SWIM_1)
                  * self.COEFF_CALORIE_SWIM_2 * self.weight)
        return result


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training = {'SWM': Swimming,
                'RUN': Running,
                'WLK': SportsWalking
                }
    try:
        return training[workout_type](*data)
    except KeyError as e:  # исключение при некорректном типе тренировки
        training_keys = training.keys()
        sensor_keys = ", ".join(training_keys)
        print(f'От датчика передано {e}. Доступные значения {sensor_keys}.')


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
        try:
            main(training)
        except AttributeError:
            pass