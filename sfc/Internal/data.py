from django.db import connection
import sys


class DataLayer:
    def createparams(self, params):
        if len(params) == 1:
            value = f"('{''.join(params)}')"
        else:
            value = f"{params}"
        return value

    def runstoredprocedure(self, spname, tparams):
        value = ''
        try:
            if len(spname) == 0:
                raise Exception('Missing data layer name element')
            if len(tparams) == 0:
                raise Exception('Missing data layer elements')
            if type(tparams) != tuple:
                raise Exception('Wrong elements data type')

            params = self.createparams(tparams)

            query = f"call {spname} {params}"
            print(query)
            cursor = connection.cursor()
            sp_result = cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                value = row[0]
            return value

        except Exception as inst:
            if (str(type(inst)) == "<class 'django.db.utils.ProgrammingError'>"):
                value = str(inst)
                if (value.find('HINT:') != -1):
                    hint = value.find('HINT:')
                    value = value[hint:len(value)]
                else:
                    value = "Something went wrong calling data layer. Call IT."
            else:
                value = str(inst)
            return str(value)

    def getfuntiontable(self, spname, params):
        value = ''
        return str(value)