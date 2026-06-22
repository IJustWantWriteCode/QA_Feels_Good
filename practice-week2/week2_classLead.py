class Lead:
    def __init__(self, name):
        self.name = name

lead = Lead('Старое имя')
print(lead.name)


def change_name(name):
    lead.name = 'Новое имя'
    print(lead.name)
change_name(lead)

print(lead.name)