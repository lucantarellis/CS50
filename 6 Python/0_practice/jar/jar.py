class Jar:
    def __init__(self, capacity=12):
        if capacity < 0:
            raise ValueError('Wrong capacity.')
        self._capacity = capacity
        self._actcap = 0

    def __str__(self):
        return "🍪" * self._actcap

    def deposit(self, n):
        if self._actcap + n <= self._capacity:
            self._actcap += n
        else:
            raise ValueError('Jar capacity exceeded.')

    def withdraw(self, n):
        if self._actcap - n < 0:
            raise ValueError('Not enough cookies in the jar.')
        else:
            self._actcap -= n

    @property
    def capacity(self):
        return self._capacity

    @property
    def size(self):
        return jar._actcap

jar = Jar()
jar.deposit(7)
jar.withdraw(2)
print(jar)