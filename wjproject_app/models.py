# Create your models here.
import mongoengine
from mongoengine.fields import DateTimeField, FileField, ImageField, IntField, StringField, FloatField


class TestModel(mongoengine.Document):

    name = StringField(max_length=21)
    age = IntField(default=0)

    meta = {'db_alias': 'default',
            'collection': 'wjproject'}

    def __str__(self) -> str:
        """
        docstring
        """
        return self.name

# 数据入库


class DataFormModel(mongoengine.Document):
    dataName = StringField(required=True)
    dataNumber = StringField(required=True)
    dataFormat = StringField(required=True)
    dataCompany = StringField(required=True)
    dataMaker = StringField(required=True)
    dataMaker2 = StringField(required=True)
    dataMaker3 = StringField(required=True)
    dataDate = StringField(required=True)
    dataScale = StringField(required=True)
    dataCoordinate = StringField(required=True)
    dataAdmin = StringField(required=True)
    dataReview = StringField(required=True)
    dataStorageCompany = StringField(required=True)
    dataStorageLocation = StringField(required=True)
    dataKeyWord1 = StringField(required=True)
    dataKeyWord2 = StringField(required=True)
    dataKeyWord3 = StringField(required=True)
    dataprojectname = StringField(required=True)
    dataLeftX = StringField(required=True)
    dataLeftY = StringField(required=True)
    dataRightX = StringField(required=True)
    dataRightY = StringField(required=True)
    # dataLeftX = FloatField(required=True)
    # dataLeftY = FloatField(required=True)
    # dataRightX = FloatField(required=True)
    # dataRightY = FloatField(required=True)
    dataIntro = StringField(required=True, max_length=128)
#     carouselImg = ImageField(db_alias='wjdataform',
#                              collection_name='fs_img')
    fileList = FileField(db_alias='wjdataform',
                         collection_name='fs_file')
    # imgList = ImageField(db_alias='wjdataform',
    #                      collection_name='fs_img')
    imgList = FileField(db_alias='wjdataform',
                         collection_name='fs_img')

    meta = {'db_alias': 'wjdataform',
            'collection': 'dataform'}

    def __str__(self) -> str:
        """
        docstring
        """
        return self.dataName
