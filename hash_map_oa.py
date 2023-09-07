# Name: Sonja Lavin
# Course: CS261 - Data Structures
# Due Date: August, 15 2023
# Description: Implementation of HashMap using Open Addressing with Quadratic Probing for
# collision resolution. Key/Value pairs stored in an array. Methods include put(), get()
# remove(), contains_key(), clear(), empty_buckets(), resize_table(), table_load(),
# get_keys(), __iter__(), __next__()

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates key/value pair in hash map. If the given key already exists in
        the hash map, it's associated value is replaced with a new value. Table
        is resized to double its current capacity when laod factor is greater than
        or equal to 0.5.
        """
        # resize when load factor is greater than or equal to 0.5
        if self.table_load() >= 0.5:
            self.resize_table(2 * self._capacity)

        # compute an initial index for element
        hash = self._hash_function(key)
        initial_index = hash % self._capacity
        index = initial_index

        # if hashmap is full at index
        if self._buckets[index] is not None:
            j = 0
            while self._buckets[index] is not None:
                if self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
                    # new value replaces old for existing key, size does not change
                    self._buckets[index].value = value
                    return
                if self._buckets[index].is_tombstone:
                    # key/value replaces tombstone
                    self._buckets[index] = HashEntry(key, value)
                    # update size
                    self._size += 1
                    return
                else:
                    j += 1
                    index = (initial_index + j**2) % self.get_capacity()

        # if index with empty spot is identified in bucket list, insert new HashEntry object
        self._buckets[index] = HashEntry(key, value)
        # update size
        self._size += 1

    def table_load(self) -> float:
        """
        Returns current hash table load factor
        """
        return self._size/self._capacity

    def empty_buckets(self) -> int:
        """
        returns number of empty buckets in hash table
        """
        return self._capacity - self._size

    def resize_table(self, new_capacity: int) -> None:
        """
        Change the capacity of the internal hash table. All existing key/value pairs
        remain in the new hash map and a re rehashed.
        """
        # if new_capacity is less than current size, do nothing
        if new_capacity < self._size:
            return

        # Set new capacity to the next prime number if it isn't already prime
        if self._is_prime(new_capacity) is True:
            self._capacity = new_capacity
        else:
            self._capacity = self._next_prime(new_capacity)

        # store current data so you can rehash
        temp = self._buckets

        # reset bucket list so info can be updated during rehash
        self._buckets = DynamicArray()
        self._size = 0

        # fill new, resized bucket list with None
        for index in range(self._capacity):
            self._buckets.append(None)

        # rehash key/value pairs into new bucket list
        for index in range(temp.length()):
            if temp[index] is not None and temp[index].is_tombstone is False:
                self.put(temp[index].key, temp[index].value)

    def get(self, key: str) -> object:
        """
        returns value associated with a given key. If the key is not in the Hashmap
        returns None.
        """
        # find index for key
        hash = self._hash_function(key)
        initial_index = hash % self._capacity

        j = 0
        index = initial_index

        while self._buckets[index] is not None:
            # if you found the key in an active/non tombstone entry
            if self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
                return self._buckets[index].value
            # if key is not found use quadratic probing to find next possible index
            j += 1
            index = (initial_index + j ** 2) % self.get_capacity()

        # if you reach an empty spot in the HashMap at or after the index
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if given key is in the hash map. Otherwise, returns False.
        """

        # an empty hash map does not contain any keys
        if self._size == 0:
            return False

        if self.get(key) is None:
            return False

        return True

    def remove(self, key: str) -> None:
        """
        removes given key and its associated value from the hash map. If the
        key is not in the hash map, does nothing.
        """

        # find index for key
        hash = self._hash_function(key)
        initial_index = hash % self._capacity
        index = initial_index
        j = 0

        while self._buckets[index] is not None:
            # if key is found
            if self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
                self._buckets[index].is_tombstone = True
                self._size -= 1
            # use quadratic probing to find next possible index
            j += 1
            index = (initial_index + j ** 2) % self.get_capacity()

        # if reached an empty index or end of list without finding key
        return

    def clear(self) -> None:
        """
        Clears contents of a hash map without changing underlying hash table capacity
        """

        self._buckets = DynamicArray()
        for index in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        returns a dynamic array where each index contains a tuple key/value pair
        stored in the hash map.
        """
        keys_and_values = DynamicArray()

        for index in range(self._buckets.length()):
            if self._buckets[index] is not None and self._buckets[index].is_tombstone is False:
                keys_and_values.append((self._buckets[index].key, self._buckets[index].value))

        return keys_and_values

    def __iter__(self):
        """
        Create iterator for loop
        """
        # tracks all indices
        self._index = 0
        return self


    def __next__(self):
        """
        Obtain next value and advance iterator
        """

        while self._index < self._capacity:

            if self._buckets[self._index] is not None and self._buckets[self._index].is_tombstone is False:
                value = self._buckets[self._index]
                self._index += 1
                return value

            self._index += 1

        # If we've reached every bucket in dynamic array, raise StopIteration
        raise StopIteration




# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(25, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(11, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)
    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.resize_table(2)
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(12)
    print(m.get_keys_and_values())

    print("\nPDF - __iter__(), __next__() example 1")
    print("---------------------")
    m = HashMap(10, hash_function_1)
    for i in range(5):
        m.put(str(i), str(i * 10))
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)


    print("\nPDF - __iter__(), __next__() example 2")
    print("---------------------")
    m = HashMap(10, hash_function_2)
    for i in range(5):
        m.put(str(i), str(i * 24))
    m.remove('0')
    m.remove('4')
    print(m)
    for item in m:
        print('K:', item.key, 'V:', item.value)
