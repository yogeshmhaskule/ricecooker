from ricecooker.classes import Channel, Video, Audio, Document, Topic, guess_content_kind
from ricecooker.exceptions import UnknownContentKindError, raise_for_invalid_channel
from fle_utils import constants

SAMPLE_TREE = [
    {
        "title": "Western Philosophy",
        "id": "abd115",
        "description": "Philosophy materials for the budding mind.",
        "children": [
            {
                "title": "Nicomachean Ethics",
                "id": "ffda92",
                "author": "Aristotle",
                "description": "The Nicomachean Ethics is the name normally given to ...",
                "file": ["https://archive.org/download/petersethics00arisrich/petersethics00arisrich.pdf"],
                "license": constants.L_PD,
            },
            {

                "title": "The Critique of Pure Reason",
                "id": "6ef99c",
                "description": "Kant saw the Critique of Pure Reason as an attempt to bridge the gap...",
                "children": [
                    {
                        "title": "01 - The Critique of Pure Reason",
                        "id": "8326cc",
                        "related_to": ["aaaa4d"],
                        "file": "https://archive.org/download/critique_pure_reason_0709_librivox/critique_of_pure_reason_01_kant.mp3",
                        "subtitle": "https://archive.org/download/critique_pure_reason_0709_librivox/critique_of_pure_reason_01_kant.vtt",
                        "author": "Immanuel Kant",
                        "license": constants.L_PD,
                    },
                    {
                        "title": "02 - Preface to the Second Edition",
                        "id": "aaaa4d",
                        "author": "Immanuel Kant",
                        "file": "https://ia801406.us.archive.org/13/items/alice_in_wonderland_librivox/wonderland_ch_01.mp3",
                        "author": "Immanuel Kant",
                        "license": constants.L_PD,
                    }
                ]
            },
        ]
    },
    {
        "title": "Recipes",
        "id": "d98752",
        "description": "Recipes for various dishes.",
        "children": [
            {
                "title": "Smoked Brisket Recipe",
                "id": "418799",
                "author": "Bradley Smoker",
                "file": "https://archive.org/download/SmokedBrisketRecipe/smokedbrisketrecipebybradleysmoker.mp4",
                "subtitle": "something.vtt",
                "license": constants.L_CC_BY,
            },
            {
                "title": "Food Mob Bites 10: Garlic Bread",
                "id": "6cafe2",
                "author": "Revision 3",
                "description": "Basic garlic bread recipe.",
                "file": "https://archive.org/download/Food_Mob_Bites_10/foodmob--bites--0010--garlicbread--hd720p30.h264.mp4",
                "license": constants.L_CC_BY_NC_SA,
            },
        ]
    },
]

def construct_channel(args):

    channel = Channel(
        domain="learningequality.org",
        channel_id="sample-channel",
        title="Sample channel",
        thumbnail="https://s.graphiq.com/sites/default/files/stories/t4/15_Tiniest_Dog_Breeds_1718_3083.jpg",
    )
    _build_tree(channel, SAMPLE_TREE)
    raise_for_invalid_channel(channel)

    return channel


def _build_tree(node, sourcetree):

    for child_source_node in sourcetree:
        try:
            kind = guess_content_kind(child_source_node.get("file"))
        except UnknownContentKindError:
            continue

        if kind == constants.CK_TOPIC:
            child_node = Topic(
                id=child_source_node["id"],
                title=child_source_node["title"],
                author=child_source_node.get("author"),
                description=child_source_node.get("description"),
            )
            node.add_child(child_node)

            source_tree_children = child_source_node.get("children", [])

            _build_tree(child_node, source_tree_children)

        elif kind == constants.CK_VIDEO:

            child_node = Video(
                id=child_source_node["id"],
                title=child_source_node["title"],
                author=child_source_node.get("author"),
                description=child_source_node.get("description"),
                files=child_source_node.get("file"),
                license=child_source_node.get("license"),

                # video-specific data
                preset=constants.FP_VIDEO_HIGH_RES,
                transcode_to_lower_resolutions=True,
                derive_thumbnail=True,

                # audio and video shared data
                subtitle=child_source_node.get("subtitle"),
            )
            node.add_child(child_node)

        elif kind == constants.CK_AUDIO:
            child_node = Audio(
                id=child_source_node["id"],
                title=child_source_node["title"],
                author=child_source_node.get("author"),
                description=child_source_node.get("description"),
                files=child_source_node.get("file"),
                license=child_source_node.get("license"),

                # audio and video shared data
                subtitle=child_source_node.get("subtitle"),
            )
            node.add_child(child_node)

        elif kind == constants.CK_DOCUMENT:
            child_node = Document(
                id=child_source_node["id"],
                title=child_source_node["title"],
                author=child_source_node.get("author"),
                description=child_source_node.get("description"),
                files=child_source_node.get("file"),
                license=child_source_node.get("license"),
            )
            node.add_child(child_node)

        else:                   # unknown content file format
            continue

    return node