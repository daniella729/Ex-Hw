def validation_generate_pyramid(height: int) -> None:
    if height < 1:
        raise ValueError("Height must be at least 1.")
    if height > 9:
        raise ValueError("Height cannot exceed 9.")


def generate_pyramid(height: int) -> str:
    validation_generate_pyramid(height)
    reslut = ""
    # to loop over the rows
    for i in range(1, height + 1):
        # to add space in the row
        reslut = reslut + " " * (height - i)
        # bulid the numeric pattren for the cuurent row
        for j in range(1, 2 * i):
            if j <= i:
                value = j
            else:
                value = 2 * i - j
            if value <= i:
                reslut = reslut + str(value)

        reslut = reslut + "\n"

    if reslut != "":
        # remove the last null row
        reslut = reslut[:-1]

    return reslut
