import requests
import re


class NinjaParser:
    currencyList = ["Currency", "Fragment"]
    itemList = ["Oil", "Incubator", "Scarab", "Fossil", "Resonator", "Essence",
                "DivinationCard", "Prophecy", "SkillGem", "BaseType", "HelmetEnchant", "UniqueMap",
                "Map", "UniqueJewel", "UniqueFlask", "UniqueWeapon", "UniqueArmour", "UniqueAccessory",
                "Beast"]

    def format(self, string):
        return string.lower().capitalize()

    def buildRegex(self, string):
        split_list = string.split(' ')
        expression = "^"
        for x in range(len(split_list)):
            if x != len(split_list) - 1:
                expression += "(?=.*" + split_list[x] + ")"
            else:
                expression += "(?=.*" + split_list[x] + ").*$"

        return re.compile(f'(%s)' % expression, re.IGNORECASE)

    def downloadItemOverviewDict(self, league_name, type):
        url = "https://poe.ninja/api/data/itemoverview?type=%s&league=%s" % (type, self.format(league_name))
        r = requests.get(url, allow_redirects=True)
        if r.status_code == 404:
            return None

        return r.json().get('lines')

    def downloadCurrencyOverviewDict(self, league_name, type):
        url = "https://poe.ninja/api/data/currencyoverview?type=%s&league=%s" % (type, self.format(league_name))
        r = requests.get(url, allow_redirects=True)
        if r.status_code == 404:
            return None
        return r.json().get('lines')

    def query(self, league_name, item_name):
        for type in self.currencyList:
            items_list = self.downloadCurrencyOverviewDict(league_name, type)

            output = self.searchCurrencyInDict(items_list, item_name)
            if output is not None:
                return output
        # print("here")
        for cat in self.itemList:
            items_list = self.downloadItemOverviewDict(league_name, cat)
            # print(cat)
            output = self.searchItemInDict(items_list, item_name)
            if output is not None:
                return output

        return None

    def searchCurrencyInDict(self, items_list, item_name):
        output = []
        coef = 0
        regex = self.buildRegex(item_name)
        for item in items_list:
            for matches in regex.findall(item.get('currencyTypeName')):
                if coef < (len(item_name) / len(item.get('currencyTypeName'))) <= 1:
                    coef = len(item_name) / len(item.get('currencyTypeName'))
                    output.clear()
                    output.append(item.get('currencyTypeName'))
                    output.append(item.get('chaosEquivalent'))
            # if regex.search(item.get('currencyTypeName')) is not None:
            #     output.append(item.get('currencyTypeName'))
            #     output.append(item.get('chaosEquivalent'))
            #     return output

        print(output)
        return output if len(output) > 0 else None

    def searchItemInDict(self, items_list, item_name):
        output = []
        regex = self.buildRegex(item_name)
        for item in items_list:
            print(regex.findall(item.get('name')))
            if regex.search(item.get('name')) is not None:
                output.append(item.get('name'))
                output.append(item.get('icon'))
                output.append(item.get('chaosValue'))
                return output

        return None
