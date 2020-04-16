import logging
import os
from datetime import datetime

import shotgun_api3
from django.conf import settings
from django.core.paginator import Paginator
from django.views.generic import TemplateView


def _get_sg_vars():
    """
    :returns: A shotgun connection object and Project dict, as a set.
    """

    # Grab a Shotgun connection.
    sg = shotgun_api3.Shotgun(
        os.environ["SG_SERVER"],
        script_name=os.environ["SG_SCRIPT_API_TEST"],
        api_key=os.environ["SG_KEY_API_TEST"],
    )
    logging.debug("Created new Shotgun connection.")

    return sg


def _set_up_logging():
    """
    Creates logs directory and sets up logging-related stuffs.
    """

    # Create a logs directory if it doesn't exist.
    log_path = os.path.join(settings.BASE_DIR, "logs")
    if not os.path.exists(log_path):
        os.makedirs(log_path)

    # Create a datestamp var for stamping the logs.
    datestamp = datetime.now().strftime("%Y_%m_%d_%H-%M-%S")

    # Create a log file path.
    log = os.path.join(log_path, "%s_%s.log" % ('views', datestamp)
                       )

    # Set the logging level.
    logging_level = logging.DEBUG

    # Set up our logging.
    logging.basicConfig(
        filename=log,
        level=logging_level,
        format="%(levelname)s: %(asctime)s: %(message)s",
    )
    logging.getLogger().addHandler(logging.StreamHandler())


class IndexView(TemplateView):
    template_name = 'sgSite/index.html'
    context_object_name = 'sgindex'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Start logging
        _set_up_logging()

        # Grab a Shotgun connection.
        try:
            sg = _get_sg_vars()
        except BaseException as e:
            logging.error("Could not create connection to Shotgun")
            context['contenttitle'] = "ERROR"
            context['content'] = "Error connecting to Shotgun Server"
            return context

        # Project fields to include
        fields = ['id', 'name']

        # Filters out only Feature type projects and no templates
        filters = [
            ['sg_type', 'is', 'Feature'],
            ['is_template', 'is', False]
        ]

        try:
            # Get list of all projects
            all_projects = sg.find('Project', filters, fields)
            logging.info("Found %s Projects.\n" % len(all_projects))

            if all_projects:
                # Send list to content to parse and display
                context['contenttitle'] = "Projects"
                context['projects'] = all_projects
            else:
                context['contenttitle'] = "Projects"
                context['projects'] = []
                context['content'] = "No projects found"

        except shotgun_api3.Fault as e:
            logging.error("Could not find Project or Shots for Project ID: %s. Error: %s" % (context['project_id'], e))

        return context


class ProjectView(TemplateView):
    template_name = 'sgSite/project.html'
    context_object_name = 'sgproject'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Start logging
        _set_up_logging()

        # Grab a Shotgun connection.
        try:
            sg = _get_sg_vars()
        except BaseException as e:
            logging.error("Could not create connection to Shotgun")
            context['title'] = "Error"
            context['contenttitle'] = "ERROR"
            context['content'] = "Error connecting to Shotgun Server"
            context['shots'] = []
            return context

        # Project fields to include
        project_fields = ['id', 'name']

        # Filter the specific project name
        project_filters = [
            ['id', 'is', context['project_id']]
        ]

        try:
            # Get list of all projects
            project = sg.find_one('Project', project_filters, project_fields)

            if project:
                # Shot fields to include
                shot_fields = ['id', 'image', 'code', 'sg_sequence', 'description']

                # Shot filters to filter to this project
                shot_filters = [
                    ['project', 'is', project]
                ]

                # Get list of shots
                shot_list = sg.find('Shot', shot_filters, shot_fields)
                logging.info("Found %s Shots in Project %s.\n" % (len(shot_list), context['project_id']))

                if shot_list:
                    # Create a Paginator object with the list and 10 shots per page
                    paginator = Paginator(shot_list, 10)

                    # Set the page variable from the url query string
                    page = self.request.GET.get('page')
                    shots = paginator.get_page(page)

                    context['title'] = project['name']
                    context['contenttitle'] = "Shots"
                    context['shots'] = shots
                else:
                    context['title'] = project['name']
                    context['contenttitle'] = "No shots found"
                    context['shots'] = []
            else:
                context['title'] = "Error"
                context['contenttitle'] = "Project not found"
                context['shots'] = []
        except shotgun_api3.Fault as e:
            logging.error("Could not find Project or Shots for Project ID: %s. Error: %s" % (context['project_id'], e))

        return context
