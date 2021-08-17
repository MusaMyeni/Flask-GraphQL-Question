import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField

from . import models, mutations
from .types import PostConnection, PostNode


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    post = graphene.Field(lambda: PostNode, createdAt=graphene.String())
    all_posts = SQLAlchemyConnectionField(PostConnection)

    def resolve_post(self, info, *args, **kwargs):
        """
        This will return the first result based on the filter.
        """
        ## Needs to return multiple results similar to result below. .all() returns error.
        query = PostNode.get_query(info) 
        created_at = kwargs.get('createdAt')
        formatted_created_at = "%{}%".format(created_at)
        return query.filter(models.Post.created_at.like(formatted_created_at)).first()

class Mutation(graphene.ObjectType):
    create_post = mutations.CreatePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)