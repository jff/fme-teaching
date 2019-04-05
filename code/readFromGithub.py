from github import Github
from fme_github_keys import fme_github_key
import json

# Luigia's github repo
courses_repo = 'luigiapetre/Formal-Methods-Courses'


def map_to_keys(field):
    # The following dictionary maps the keys used in Github issues
    # to the keys that we want to use internally (e.g. in the json data)
    d = {'Course code, if applicable': 'course_code',
         'University hosting the course': 'course_institution',
         'Contact person': 'course_contact',
         'Concepts taught': 'course_concepts',
         'Tools used': 'course_tools',
         'Webpage': 'course_webpage'
         }
    if field not in d:
        d[field] = ''
    return d[field]


def process_issue_body(issue_body):
    """ Each issue corresponds to a course.
    This function extracts the information from the issue body
    and creates a dictionary with that information.

    We assume the following order of fields (keys):
        - Course code, if applicable:
        - University hosting the course
        - Contact person
        - Concepts taught
        - Tools used
        - Webpage
    """

    # We first create a list with elements of type (name, [[key, value]])
    flist = filter(lambda f: len(f) == 2,
                   map(lambda f: f.split(': '), issue_body.split('\r\n')))

    # We now normalise the keys
    flist_norm = map(lambda pair: [map_to_keys(pair[0]), pair[1].strip()],
                     flist)

    return dict(flist_norm)


def standardise_keyword(word):
    """ The idea is to define here all the transformations that we want
    to do so that keywords are uniform. For example, 'hoare logic' and
    'Hoare logic' are both mapped to 'Hoare Logic'.
    """
    new_word = word.strip().title()
    return new_word


def create_list_courses(courses_repo, fme_github_key):
    # Create access based on the key provided
    g = Github(fme_github_key)

    # Get all courses (open issues)
    repo = g.get_repo(courses_repo)
    open_issues = repo.get_issues(state='open')

    courses = []
    for issue in open_issues:
            course = process_issue_body(issue.body)
            course['course_title'] = issue.title

            if issue.labels:
                course['course_country'] = issue.labels[0].name

            # Change string of tools and concepts to list
            if 'course_concepts' in course and course['course_concepts']:
                concepts = course['course_concepts']
                concepts = list(map(lambda s: standardise_keyword(s),
                                    concepts.split(',')))
                course['course_concepts'] = concepts
            else:
                course['course_concepts'] = ["Unknown"]
            if 'course_tools' in course and course['course_tools']:
                tools = course['course_tools']
                tools = list(map(lambda s: standardise_keyword(s),
                                 tools.split(',')))
                course['course_tools'] = tools
            else:
                course['course_tools'] = ["Unknown"]

            # Check whether the institution is defined
            if 'course_institution' not in course or \
               course['course_institution']:
                course['course_institution'] = ["Unknown"]

            # Check whether the webpage is defined and remove trailing /
            if 'course_webpage' not in course:  # or course['course_webpage']:
                course['course_webpage'] = "#"
            else:
                webpage = course['course_webpage']
                if len(webpage) > 0 and webpage[-1] == '/':
                    course['course_webpage'] = webpage[:-1]

            # Remove email address from contact. TODO: confirm
            if 'course_contact' in course:
                contact = course['course_contact']
                contact = contact.split(',')[0]
                course['course_contact'] = contact

            courses.append(course.copy())

    return courses


def list_by_key(list_courses, key):
    """ Given a list of courses (as dictionaries) and a key, this 
    function returns a sorted list of all the 'keys' used.
    """
    concepts = []
    for course in list_courses:
        concepts.extend(course[key])
    concepts = list(set(concepts))
    concepts.sort()
    return concepts


def list_of_countries(list_courses):
    """ Given a list of courses (as dictionaries), this function
    returns a sorted list of all the countries used.
    """
    countries = []
    for course in list_courses:
        # IMPORTANT: note the use of lists for course_country
        countries.extend([course['course_country']])
    countries = list(set(countries))
    countries.sort()
    return countries


# Driver code below

courses = create_list_courses(courses_repo, fme_github_key)
courses_json = json.dumps(courses, indent=4)

concepts = list_by_key(courses, 'course_concepts')
concepts_json = json.dumps(concepts, indent=4)

tools = list_by_key(courses, 'course_tools')
tools_json = json.dumps(tools, indent=4)

countries = list_of_countries(courses)
countries_json = json.dumps(countries, indent=4)


# Write to file
f_out = open('fme-courses-github.js', 'w')
f_out.write('var courses = \n')
f_out.write(courses_json)
f_out.write('\nvar concepts = \n')
f_out.write(concepts_json)
f_out.write('\nvar tools = \n')
f_out.write(tools_json)
f_out.write('\nvar countries = \n')
f_out.write(countries_json)
f_out.close()
