# Руководство разработчика
## Оглавление 
* [Модели](#модели)
  * [Документ](#документ)
  * [Ресурс документа](#ресурс-документа)
    * [Функия: путь к файлу](#функция-путь-к-файлу)
  * [Папка](#папка)
  * [Разрешение документа](#разрешение-документа)
  * [РазрешениеПапки](#разрешение-папки)
* [Сериализаторы](#сериализаторы)
  * [Документ](#документ-1)
    * [Создание документа и ресурса](#создание-документа-и-ресурса)
    * [Изменение документа и ресурса](#изменение-документа-и-ресурса)
    * [Получение документа](#получение-документа)
  * [Папка](#папка-1)
    * [Создание папки](#создание-папки)
    * [Изменение папки](#изменение-папки)
    * [Получение папки](#получение-папки)
  * [Разрешение](#разрешение)
    * [Документ](#документ-2)
    * [Папка](#папка-2)
* [View функции](#view-функции)
  * [Документ](https://github.com/Mans-Mans/hw_python_oop/tree/master?tab=readme-ov-file#документ-3)
    * [Создание документа](#создание-документа)
    * [Просмотр документа](#просмотр-документа)
    * [Удаление документа](#удаление-документа)
    * [Редактирование документа](#редактирование-документа)
  * [Ресурс документа]
    * [Создание ресурса]
      * [Привязка ресурса к документу]
    * [Удаление ресурса]
    * [Изменение ресурса]
      * [Изменение связи ресурс-документ]
  * [Папка]
    * [Создание папки]
    * [Просмотр папки]
    * [Удаление папки]
    * [Редактирование папки]
  * [Разрешение]
    * [Создание разрешения]
    * [Удаление разрешения]
    * [Просмотр разрешений]
* [URL адреса]
  * [Документ]
  * [Ресурс документа]
  * [Папка]
  * [Разрешения]
* [Панель админа]
  * [Документы]
  * [Ресурсы документа]
  * [Папки]
  * [Разрешения]
## <a>Модели</a>
* ### <a>Документ</a>
Модель документа наследуется от базовой модели модуля ib_core и имеет __одно обязательное__ поле: название; и __пять необязательных__ полей: описание, ресурсы, активная версия ресурса, папка(расположение документа), разрешенные пользователи. Используется для всех операции связанных с документами.
````
class Document(UUIDModel):
    """Модель документа.\n
    Обьект этой модели вернет его UUID.
    Значение folder хранит UUID папки, в которой распологается документ.
    Если folder is None значит документ находится на главной странице
    пользователя."""
    name = models.CharField(max_length=255, verbose_name="Название документа")
    description = models.TextField(null=True,
                                   blank=True,
                                   verbose_name="Описание")
    resources = OneToManyField(
        "documents_management.DocumentResource",
        verbose_name="Ресурсы",
        blank=True,
    )
    active_version = models.ForeignKey(
        "documents_management.DocumentResource",
        verbose_name="",
        null=True, blank=True,
        related_name='active',
        on_delete=models.SET_NULL
    )
    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        verbose_name="Расположение документа",
        related_name='documents_folder',
        blank=True, null=True,
    )
    allowed_user = OneToManyField(
        DocumentPermission,
        verbose_name="Разрешенные пользователи",
        blank=True,
        related_name="allowed_user_document"
    )

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"

    def __str__(self):
        return f"{self.pk}"

    def is_creator(self, user_id: str):
        return str(self.creator) == user_id

    def full_to_dict(self):
        return {
            "id": self.pk,
            "name": self.name,
            "description": self.description,
            "creator": self.creator,
            "folder": self.folder.id if self.folder else None,
            "active_version": self.active_version.id if
            self.active_version else None,
            "resources": [resource.id for resource in
                          list(self.resources.all())]
        }
````
* ### <a>Ресурс Документа</a>
Модель ресурс документа наследуется от базовой модели модуля ib_core и имеет __два обязательных__ поля: документ, файл. Используется для создания файла и привязки к определенному документу. Место установки файла описано в функции document_resource_file_path().
````
class DocumentResource(UUIDModel):
    """Модель ресурса.\n
    Возвращает UUID ресурса и UUID документа к которому привязан."""
    related_document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        verbose_name="Документ")
    file = models.FileField(
        upload_to=document_resource_file_path)

    class Meta:
        verbose_name = "Ресурс документа"
        verbose_name_plural = "Ресурсы документов"

    def to_dict(self):
        return {
            "id": self.pk,
            "related_document": str(self.related_document),
            "file": self.file
        }

    def __str__(self):
        return f"{self.pk}"
````
#### <a>Функция: путь к файлу</a>
Эта функция сохраняет файл по пути media/documents/{UUIDДокмента}/{name} и устанавливает ему название{name} в формате "НазваниефайлаДатаРасширениефайла".
````
def document_resource_file_path(instance, filename):
    name, extension = os.path.splitext(filename)
    return 'media/documents/{0}/{1}{2}'.format(
        instance.related_document.pk,
        f"{str(name)}{datetime.now().strftime('%Y%m%d%H%M%S')}",
        str(extension)
    )
````
* ### <a>Папка</a>
Модель папка наследуется от базовой модели модуля ib_core и имеет __одно обязательное__ поле: название; и __три необязательных__ поля: документы, локация(расположение папки), разрешенные пользователи. Используется для всех операции связанных с папками.
````
class Folder(UUIDModel):
    """Модель папки.\n
    Обьект модели возвращает его PK.\n
    Значение location хранит UUID папки, в которой распологается текущая
    папка. Если location пустая значит папка находится на главной странице
    пользователя."""
    name = models.CharField(max_length=255, verbose_name="Название папки")
    documents = OneToManyField(
        "documents_management.Document",
        verbose_name="Документы",
        related_name="documents",
        blank=True,
    )
    location = models.UUIDField(
        verbose_name="Расположение папки",
        blank=True, null=True,
    )
    allowed_user = OneToManyField(
        FolderPermission,
        verbose_name="Разрешенные пользователи",
        blank=True,
        related_name="allowed_user_folder"
    )

    class Meta:
        verbose_name = "Папка"
        verbose_name_plural = "Папки"

    def __str__(self):
        return f"{self.pk}"

    def is_creator(self, user_id: str):
        return str(self.creator) == user_id

    def to_dict(self):
        return {
            "id": self.pk,
            "name": self.name,
            "location": self.location,
            "documents": [document.id for document in
                          list(self.documents.all())]
        }
````
* ### <a>Разрешение документа</a>
Модель наследуется от базовой модели модуля ib_core и имеет __два обязательных__ поля: документ, пользователь. Используется для операции доступа к документу выбранного пользователя.
````
class DocumentPermission(UUIDModel):
    """Модель доступа к документам.\n
    Хранит информацию о предоставленных доступах к документам
    определенным пользователям."""
    document = models.ForeignKey(
        "documents_management.Document",
        on_delete=models.CASCADE,
        verbose_name="Документ",
        related_name="document_permission"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        blank=True,
        related_name="allowed_doc_user"
    )

    class Meta:
        verbose_name = "Доступ к документу"
        verbose_name_plural = "Доступы к документам"
        unique_together = [
            ["document", "user"]
        ]

    def to_dict(self):
        return {
            "user": self.user.id,
            "document": self.document
        }

    def __str__(self):
        return f"Permission {self.user} for document {self.document.pk}"
````
* ### <a>Разрешение папки</a>
Модель наследуется от базовой модели модуля ib_core и имеет __два обязательных__ поля: папка, пользователь. Используется для операции доступа к папке выбранного пользователя.
````
class FolderPermission(UUIDModel):
    """Модель доступа к папкам.\n
    Хранит информацию о предоставленных доступах к папкам
    определенным пользователям."""
    folder = models.ForeignKey(
        "folders_management.Folder",
        on_delete=models.CASCADE,
        verbose_name="Папка",
        related_name="folder_permission"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        blank=True,
        related_name="allowed_folder_user"
    )

    class Meta:
        verbose_name = "Доступ к папке"
        verbose_name_plural = "Доступы к папкам"
        unique_together = [
            ["folder", "user"]
        ]

    def to_dict(self):
        return {
            "user": self.user.id,
            "folder": self.folder
        }

    def __str__(self):
        return f"Permission {self.user} for folder {self.folder.pk}"
````
## <a>Сериализаторы</a>
* ### <a>Документ</a>
#### <a>Создание документа и ресурса</a>
````
class DocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["id", "name", "description", "folder",
                  "creator", "active_version", "resources"]
        read_only_fields = ("folder", "creator",
                            "active_version", "resources")
````
````
class DocumentResourceCreateSerializer(serializers.ModelSerializer):
    set_active = serializers.BooleanField(default=False)
    class Meta:
        model = DocumentResource
        fields = ["id", "file", "related_document", "set_active"]
        read_only_fields = ("related_document",)
````
#### <a>Изменение документа и ресурса</a>
  При изменение документа происходит валидация параметров name и folder. Не допускается одинакового названии двух документов в одной и той же папке.
````
class DocumentUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, max_length=155)
    class Meta:
        model = Document
        fields = ("id", "name", "description", "folder", "creator",
                  "active_version", "resources")
        read_only_fields = ("creator", "active_version",
                            "resources",)
        validators = [
            UniqueTogetherValidator(
                queryset=Document.objects.all(),
                fields=('name', 'folder'),
                message='Document with name already exsists in this folder.'
            )
        ]
````
````
class RebindDocumentResourceSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    document = serializers.UUIDField(write_only=True)
    set_active = serializers.BooleanField(default=True)
    filename = serializers.CharField(read_only=True)
````
#### <a>Получение документа</a>
DocumentSerializer используется как дополнительный сериализатор, при сериализации всех документов при отображении содержимого [папки](#получение-папки).
````
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ("id", "name")
````
DocumentByIDSerializer используется при отображении конкретного документа по его ID.
````
class DocumentByIDSerializer(serializers.ModelSerializer):
    resources = DocumentResourceSerializer(required=False, many=True)
    class Meta:
        model = Document
        fields = ("creator", "name", "folder",
                  "description", "resources", "active_version")
````
Значение resources сериализуется при помощи дополнительного сериализатора документ ресурс.
````
class DocumentResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentResource
        fields = ("id", "file")
````
* ### <a>Папка</a>
#### <a>Создание папки</a>
````
class FolderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ("id", "name", "location", "documents")
        read_only_fields = ("documents",)
````
#### <a>Изменение папки</a>
При изменение папки происходит валидация параметров name и location. Не допускается одинакового названии двух папок в одной и той же папке.
````
class FolderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ("id", "name", "location", "documents",)
        read_only_fields = ("location", "documents",)
        validators = [
            UniqueTogetherValidator(
                queryset=Folder.objects.all(),
                fields=('name', 'location'),
                message='Folder with name already exsists in this folder.'
            )
        ]
````
#### <a>Получение папки</a>
FolderSerializer используется как дополнительный сериализатор, при сериализации всех папок при отображении содержимого папки.
````
class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ("id", "name",)
````
FoldersAndDocumentsSerializer используется при отображении содержимого папки.
````
class FoldersAndDocumentsSerializer(serializers.Serializer):
    folders = FolderSerializer(required=False, many=True)
    documents = DocumentSerializer(required=False, many=True)
````
* ### <a>Разрешение</a>
#### <a>Документ</a>
````
class DocumentPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentPermission
        fields = ("user",)
````
#### <a>Папка</a>
````
class FolderPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FolderPermission
        fields = ("user",)
````
## <a>View функции</a>
* ### <a>Документ</a>
#### <a>Создание документа</a>
````
class DocumentCreateAPIView(TokenAuthorizationMixin, generics.CreateAPIView):
    """Создание документа.\n
    По эндпоинту "/api/document/create" документ
    создаётся без расположения в папке,
    то есть на главной странице пользователя.\n
    По эндпоинту "/api/document/create-in-folder/{id}"
    документ создаётся в папке.
    В пути запроса указывается {id} папки, в которой создаётся документ.\n
    Доступ: все авторизованные пользователи.\n
    """
    serializer_class = DocumentCreateSerializer
    queryset = Folder.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if kwargs:
            folder = Folder.objects.get(pk=str(kwargs["pk"]))
        else:
            folder = None
        if Document.objects.filter(
            name=serializer.validated_data.get("name"),
                folder=folder).exists():
            return Response(
                data={"Errod": "Document with name already"
                      "exists in this folder."}
            )
        document = Document.objects.create(
            name=serializer.validated_data.get("name"),
            description=serializer.validated_data.get("description"),
            folder=folder,
            creator=self.request.user.id
        )
        if folder is not None:
            folder.documents.add(document)
        return Response(document.full_to_dict(),
                        status=status.HTTP_201_CREATED)
````
#### <a>Просмотр документа</a>
````
class GetDocumentByIDAPIView(TokenAuthorizationMixin, generics.RetrieveAPIView):
    """Отображение документа.\n
    По эндпоинту "/api/document/getting/{id}" отображается документ.\n
    В пути запроса указывается {id} документа, который нужно отобразить.\n
    Доступ: создатель документа или разрешенные пользователи.\n
    """
    serializer_class = DocumentByIDSerializer
    queryset = Document.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsCreatorOrAllowedUser,)

    def get(self, *args, **kwargs):
        obj = self.get_object()
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
````
#### <a>Удаление документа</a>
````
class DestroyDocumentAPIView(TokenAuthorizationMixin, generics.DestroyAPIView):
    """Удаление документа.\n
    По эндпоинту "/api/document/deleting/{id}" удаляется документ.\n
    В пути запроса указывается {id} документа, который нужно удалить.\n
    Доступ: создателю документа.\n
    """
    queryset = Document.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsCreator,)

    def delete(self, *args, **kwargs):
        delete_document = self.get_object()
        if delete_document:
            resource = DocumentResource.objects.all().filter(
                related_document=delete_document)
            delete_document.delete()
            resource.delete()
            return Response(data={"Done": "The document has been deleted."},
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data={"Error": "Document not found."},
                            status=status.HTTP_404_NOT_FOUND)
````
#### <a>Редактирование документа</a>
````
class DocumentUpdateAPIView(TokenAuthorizationMixin, generics.UpdateAPIView):
    """Изменение документа.\n
    По эндпоинту "/api/document/updating/{id}" изменяется документ.\n
    В пути запроса указывается {id} документа, который нужно изменить.\n
    Доступ: создателю документа.\n
    """
    serializer_class = DocumentUpdateSerializer
    queryset = Document.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsCreator,)

    def update(self, request, **kwargs):
        partial = kwargs.pop('partial', False)
        document = self.get_object()
        serializer = self.serializer_class(document,
                                           data=request.data,
                                           partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(document.full_to_dict(),
                        status=status.HTTP_200_OK)

    def put(self, request, **kwargs):
        return self.update(request, **kwargs)

    def patch(self, request, **kwargs):
        return self.partial_update(request, **kwargs)
````
* ### <a>Ресурс документа</a>
