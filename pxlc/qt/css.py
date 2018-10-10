
def wdg_add_classes( q_wdg, css_classes_str ):

    css_class_list = css_class_str.split()
    for css_class in css_class_list:
        q_wdg.setProperty('css{}'.format(css_class), 'on')


def wdg_remove_classes( q_wdg, css_classes_str ):

    css_class_list = css_classes_str.split()
    for css_class in css_class_list:
        q_wdg.setProperty('css{}'.format(css_class), 'off')


def wdg_set_classes( q_wdg, css_classes_str ):

    for prop_name in q_wdg.dynamicPropertyNames():
        # NOTE: prop_name needs to be cast to str for .setProperty() and value None will remove property
        q_wdg.setProperty(str(prop_name), None)

    css_class_list = css_classes_str.split()
    for css_class in css_class_list:
        q_wdg.setProperty('css{}'.format(css_class), 'on')


