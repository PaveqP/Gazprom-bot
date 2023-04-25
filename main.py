import pymysql
import pymysql.cursors

from config import host

techno_id = 0


def get_currentId(current_id):
    global techno_id
    techno_id = current_id
    print(techno_id)
    return techno_id


try:
    connection = pymysql.connect(
        host=host,
        port=3306,
        database='it_time',
        user='root',
        password='1111',
        cursorclass=pymysql.cursors.DictCursor
    )
    print('Connected was successful')
    print('-/-' * 40)
    print('bot was runned')
    print('-/-' * 40)

    # получение функциональных групп
    def get_funcGroups():
        try:
            func_groups = []
            with connection.cursor() as cursor:
                get_all_table_query = "SELECT * FROM `functional_group`"
                cursor.execute(get_all_table_query)
                rows = cursor.fetchall()
                for row in rows:
                    func_groups.append(row)

                print('=' * 20)
                return func_groups
        except:
            print('error in getting gropus')
            return 'error'


    def get_domains(id):
        try:
            # получение доменов
            all_domains = []
            with connection.cursor() as cursor:
                get_domain = f"select d.domain from main_new inner join domain d on main_new.domain_ru = d.id where functional_group = {id} group by domain_ru"
                cursor.execute(get_domain)
                domains = cursor.fetchall()
                for domain in domains:
                    all_domains.append(domain)
                print('=' * 20)
                #print(all_domains, 'ad')
                return all_domains
        except:
            print('error in getting domains')
            return 'error'


    # получение технологий
    def selectTechnos(domen_id, group_id):
        try:
            with connection.cursor() as cursor:
                get_techno = f"select tn.name from main_new inner join domain d on main_new.domain_ru = d.id join technology_new tn on main_new.technology_ru = tn.id where d.id = {domen_id} and main_new.functional_group = {group_id} group by tn.name"
                cursor.execute(get_techno)
                technos = cursor.fetchall()
                #print(technos)
                print('=' * 20)
            return technos
        except:
            print('error in getting domains')
            return 'error'

    # получение метода использования

    def selectMethods(technology_id, domen_id, group_id):
        try:
            with connection.cursor() as cursor:
                get_method = f"select am.name from main_new inner join domain d on main_new.domain_ru = d.id join technology_new tn on main_new.technology_ru = tn.id join application_method am on am.id = main_new.application_method_ru where d.id = {domen_id} and main_new.functional_group = {group_id} and technology_ru = {technology_id} group by am.name"
                cursor.execute(get_method)
                methods = cursor.fetchall()
                #print(methods)
                print('=' * 20)
            return methods
        except:
            print('error in getting domains')
            return 'error'
        
    def selectScenariosNames():
        try:
            with connection.cursor() as cursor:
                get_scenario = f"select id, scenario_name_ru from main_new"
                cursor.execute(get_scenario)
                scenariosNames = cursor.fetchall()
                #print(scenariosNames)
                print('=' * 20)
            return scenariosNames
        except:
            print('error in getting domains')
            return 'error'

    def selectScenarios(method_id, technology_id, domen_id, group_id):
        try:
            with connection.cursor() as cursor:
                get_scenario = f"select main_new.id, scenario_name_ru from \
                main_new inner join domain d on main_new.domain_ru = d.id join technology_new \
                tn on main_new.technology_ru = tn.id join application_method am on am.id = main_new.application_method_ru \
                where d.id = {domen_id} and main_new.functional_group = {group_id} and technology_ru = {technology_id} and am.id = {method_id}"
                cursor.execute(get_scenario)
                scenarios = cursor.fetchall()
                #print(scenarios)
                print('=' * 20)
            return scenarios
        except:
            print('error in getting domains')
            return 'error'
        
    def getAllInfo(scenary_id):
        try:
            with connection.cursor() as cursor:
                get_scenario = f"select scenario_name_ru, description_ru, r.solution_potential_grade, r.solution_potential_ru, \
                r.solution_maturity_grade, r.solution_maturity_ru, r.implemented_in_gazprom_ru, r.readiness_of_the_company_grade,\
                r.readiness_of_the_company_ru, b.name as \"benchmarking_name\", b.description as \"benchmarking_description\", b.company as \"benchmarking_company\",\
                b.year_of_deploy as \"benchmarking_year_of_deploy\", rad.name as \"rad_name\", rad.description as \"rad_description\", tc.name as \"tc_name\" from main_new inner join relevance r on main_new.relevance_id = r.id\
                join benchmarking b on main_new.benchmarking_id = b.id join research_and_development_projects rad on main_new.RAD_id = rad.id join technology_center tc on tc.id = main_new.tc_id\
                where main_new.id = {scenary_id}"
                cursor.execute(get_scenario)
                info = cursor.fetchall()
                #print(info)
                print('=' * 20)
            return info
        except:
            print('error in getting domains')
            return 'error'




except Exception as ex:
    print('Connection was failed...')
    print(ex)
