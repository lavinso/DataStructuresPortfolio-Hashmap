# Name: Sonja Lavin
# OSU Email: lavinso@oregonsate.edu
# Course: CS261 - Data Structures
# Assignment: 6 HashMap Implementation
# Due Date: August, 15 2023
# Description: Implementation of HashMap using Dynamic Array as underlying data
# structure and singly linked list with each node storing a key/value pair to
# chain for collision. Contains the following methods: put(), get(), remove(),
# contains_key(), clear(), empty_buckets(), resize_table(), table_load(),
# get_keys(), find_mode(). The average time complexity of all operations is O(1).

from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

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
        Increment from given number and the find the closest prime number
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
        Updates the key/value pair in the hash map. If the given key already exists
        in the hash map, it's associated value is replaced with the new value.
        If the given key is not in the hash map, a new key/value pair is added.
        Table is resized to double its current capacity when current load factor
        is greater than or equal to 1.0.
        """

        # resize when load factor is greater than or equal to one
        if self.table_load() >= 1:
            self.resize_table(2 * self._capacity)

        # run key through hash function and calculate index:
        hash = self._hash_function(key)
        index = hash % self._capacity

        # if key is already in index, replace value:
        if self._buckets[index].contains(key) is not None:
            self._buckets[index].contains(key).value = value
        else:
            # add key/value node to linked list, sets node as head, and updates SLL size
            self._buckets[index].insert(key, value)
            # update size of dynamic array/buckets
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        """
        count = 0

        for index in range(self._buckets.length()):
            if self._buckets[index].length() == 0:
                count += 1

        return count

    def table_load(self) -> float:
        """
        Returns the current hash table load factor
        """
        return self._size/self._capacity

    def clear(self) -> None:
        """
        Clears the contents of Hash map without changing underlying hash table capacity
        """
        # iterate through bucket List and replace each index with empty linked list
        for index in range(self._buckets.length()):
            self._buckets[index] = LinkedList()
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table. New_capacity passed through
        this function is double the old capacity. All existing key/value pairs
        remain in the new hash map an all hash table links are rehashed.
        """
        # if new_capacity is less than 1, return
        if new_capacity < 1:
            return

        # Set new capacity to the next prime number if it isn't already prime
        if self._is_prime(new_capacity) is True:
            self._capacity = new_capacity
        else:
            self._capacity = self._next_prime(new_capacity)

        # store current data so you can rehash
        temp = self._buckets

        # reset bucket list and size so info can be updated during rehash
        self._buckets = DynamicArray()
        self._size = 0

        # fill new, resized bucket list with empty linked lists
        for index in range(self._capacity):
            self._buckets.append(LinkedList())

        # rehash key/value pairs into new bucket list
        for index in range(temp.length()):
            if temp[index].length() != 0:
                for node in temp[index]:
                    self.put(node.key, node.value)

    def get(self, key: str):
        """
        returns the value associated with a given key.
        If key is not in the hash map returns None
        """
        # find index for key
        hash = self._hash_function(key)
        index = hash % self._capacity

        # if key is not in linked list:
        if self._buckets[index].contains(key) is None:
            return None

        # else return the value
        return self._buckets[index].contains(key).value

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map. Otherwise, returns False
        """
        # if hash map is empty, return False
        if self._size == 0:
            return False

        if self.get(key) is None:
            return False

        return True

    def remove(self, key: str) -> None:
        """
        Removes a given key and its associated value from the hash map.
        """
        # find index for key
        hash = self._hash_function(key)
        index = hash % self._capacity

        if self._buckets[index].remove(key):
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a tuple of a key/value
        pair stored in the hash map.
        """

        keys_and_values = DynamicArray()

        for index in range(self._buckets.length()):
            if self._buckets[index].length() != 0:
                for node in self._buckets[index]:
                    key = node.key
                    value = node.value
                    keys_and_values.append((key, value))

        return keys_and_values


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    parameter: unsorted DynamicArray of string elements
    returns: tuple (most occurring value(s), highest frequency of occurrence)
    O(N)
    """

    map = HashMap()

    # hashmap key: the element in the da, value: element's frequency
    for index in range(da.length()):
        # if element is already a key in the hashmap, increment frequency by 1
        if map.contains_key(da[index]):
            map.put(da[index], map.get(da[index]) + 1)
        else:
            # if the element is not a key in the hashmap, add it with a frequency of 1
            map.put(da[index], 1)

    mode = DynamicArray()
    mode_frequency = 0

    # iterate through the HashMap list of keys and values to find mode
    for index in range(map.get_keys_and_values().length()):
        tuple = map.get_keys_and_values()[index]
        element, frequency = tuple
        if frequency == mode_frequency:
            mode.append(element)
        elif frequency > mode_frequency:
            mode_frequency = frequency
            mode = DynamicArray()
            mode.append(element)

    return mode, mode_frequency

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
    """
    """
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
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

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
    m = HashMap(53, hash_function_1)
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

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
