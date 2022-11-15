def rupiah_format(angka, with_prefix) -> str :

    str_value = str(angka)

    separate_decimal = str_value.split(".")
    after_decimal    = separate_decimal[0]

    reverse = after_decimal[::-1]
    
    temp_reverse_value = ""

    for index, val in enumerate(reverse):
        if (index + 1) % 3 == 0 and index + 1 != len(reverse):
            temp_reverse_value += val + "."
        else:
            temp_reverse_value += val

    temp_result = temp_reverse_value[::-1]

    if with_prefix :

        return "Rp. " + temp_result + ",00"

    else :

        return temp_result + ",00"



def rupiah_str_to_int(rupiah_format) -> int :

    decimal_sort = rupiah_format[0:len(rupiah_format)-3]

    int_format = ""

    for index_int_format in range( len(decimal_sort) ) :

        try :

            convert_int = int( decimal_sort[index_int_format] )
            int_format += str( convert_int )

        except ValueError :

            pass

    return int( int_format )