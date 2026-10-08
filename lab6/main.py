from dataclasses import dataclass, replace


@dataclass
class OpticalDisc:
    capacity_bytes: int
    rpm: float
    laser_width_nm: float

    def __post_init__(self):
        if min(self.capacity_bytes, self.rpm, self.laser_width_nm) <= 0:
            raise ValueError("Параметры диска должны быть положительными")

    def bytes_in_20_seconds(self):
        tracks = (58 - 25) * 1_000_000 / self.laser_width_nm
        bytes_per_turn = self.capacity_bytes / tracks
        return round(bytes_per_turn * self.rpm / 60 * 20)

    def turn_seconds(self):
        return 60 / self.rpm

    def __add__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        return replace(self, capacity_bytes=self.capacity_bytes + other.capacity_bytes)


@dataclass
class CD(OpticalDisc):
    audio_minutes: int

    def bytes_in_20_seconds(self):
        return min(super().bytes_in_20_seconds(), self.capacity_bytes)


@dataclass
class DVD(OpticalDisc):
    layers: int

    def bytes_in_20_seconds(self):
        if self.layers < 1:
            raise ValueError("Нужен хотя бы один слой")
        return min(super().bytes_in_20_seconds() * self.layers, self.capacity_bytes)


def main():
    discs = [
        CD(700_000_000, 500, 1600, 80),
        DVD(4_700_000_000, 1400, 740, 1),
    ]
    for disc in discs:
        print(f"{type(disc).__name__}: {disc.bytes_in_20_seconds():,} байт за 20 с; "
              f"оборот занимает {disc.turn_seconds():.4f} с")
    print("Суммарная ёмкость двух CD:", (discs[0] + CD(700_000_000, 500, 1600, 80)).capacity_bytes)


if __name__ == "__main__":
    main()
