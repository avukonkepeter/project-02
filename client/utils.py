def id_validator(id_number: [str, int]) -> bool:
    if type(id_number) == int:
        try:
            id_number = str(id_number)
        except Exception as e:
            return False

    is_valid = False
    try:
        if id_number is None:
            return is_valid
        if isinstance(id_number, str) and id_number.find(' ') >= 0:
            id_number = id_number.replace(' ', '')
        is_valid = id_number.isdigit() and len(id_number) == 13
        if is_valid:
            index = 1
            evens = ""
            num_array = list(id_number)
            total = 0
            while index < 13:
                if index % 2 == 0:
                    evens = evens + num_array[index - 1]
                else:
                    total = total + int(num_array[index - 1])
                index = index + 1
            evensArr = list(str(int(evens) * 2))
            evenTotalArrSum = sum(int(val) for val in evensArr)
            evenOdd = total + evenTotalArrSum
            evenOddsArr = list(str(evenOdd))
            is_valid = int(num_array[12]) == 10 - int(evenOddsArr[1])
        return is_valid
    except Exception as e:
        is_valid = False
        return is_valid
