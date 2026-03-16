
def compressedString(message):

    answer = []

    i = 0

    while i < len(message):

        count = 1
        answer.append(message[i])

        while i+ 1 < len(message) and message[i] == message[i+1]:
            count += 1
            i += 1
        
        if count > 1:
            answer.append(str(count))
        
        i +=1


    return "".join(answer)

print(compressedString("aabbccca"))