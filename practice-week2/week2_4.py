def words_longer_five(word_list):
    return [word for word in word_list if len(word) > 5]

print(words_longer_five(['Go', 'Java', 'Python', 'C++', 'Rust', 'Pascal', 'Assembler']))