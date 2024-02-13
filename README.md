# Руководство разработчика
## Оглавление 
* [Модели](#модели)
  * [Документ](#документ)
  * [Ресурс документа](#ресурс-документа)
    * [Путь к файлу](#путь-к-файлу)
  * [Папка](#папка)
  * [Разрешение документа](#разрешение-документа)
  * [Разрешение Папки](#разрешение-папки)
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
    * [Изменение документа](#изменение-документа)
  * [Ресурс документа](#ресурс-документа-1)
    * [Создание ресурса](#создание-ресурса)
      * [Привязка ресурса к документу](#привязка-ресурса-к-документу)
    * [Удаление ресурса](#удаление-ресурса)
    * [Изменение ресурса](#изменение-ресурса)
      * [Изменение связи ресурс-документ](#изменение-связи-ресурс-документ)
  * [Папка](#папка-3)
    * [Создание папки](#создание-папки-1)
    * [Просмотр папки](#просмотр-папки)
    * [Удаление папки](#удаление-папки)
    * [Изменение папки](#изменение-папки-1)
  * [Разрешение](#разрешение-1)
    * [Создание разрешения](#создание-разрешения)
    * [Удаление разрешения](#удаление-разрешения)
    * [Просмотр разрешений](#просмотр-разрешения)
* [Панель админа](#панель-админа)
  * [Документы](#документы)
  * [Документ ресурсы](#документ-ресурсы)
  * [Папки](#папки)
  * [Разрешение документов](#разрешение-документов)
  * [Разрешение папок](#разрешение-папок)
  * [Инструкция запуска сервера локально](#инструкция-запуска-сервера-локально)
  * [Инструкция запуска удаленно на сервере](#инструкция-запуска-удаленно-на-сервере)
* [API](#api)
  * [Статическая документация](#статическая-api-документация)
  * [Динамическая документация](#динамическая-api-документация)
  * [Инструцкия по работе с API](#инструкция-по-работе-с-api)
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
#### <a>Путь к файлу</a>
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
#### <a>Изменение документа</a>
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
#### <a>Создание ресурса</a>
````
class DocumentResourceCreateAPIView(TokenAuthorizationMixin, generics.CreateAPIView):
    """Создание ресурса документа.\n
    По эндпоинту "resource/create/{id}" создаётся ресурс в документе.\n
    В пути запроса указывается {id} документа, в которой создаётся ресурс.\n
    Доступ: создателю документа, в которой создаётся ресурс.\n
    """
    queryset = Document.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsCreator,)
    serializer_class = DocumentResourceCreateSerializer

    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        document = self.get_object()
        if document:
            resource = bind_resource_to_document(
                document=document,
                file=serializer.validated_data.get("file"),
                creator_id=self.request.user.id,
                set_active=serializer.validated_data.get("set_active")
            )
            headers = self.get_success_headers(serializer.data)
            return Response(
                {"id": resource.id,
                 "file": resource.file.url,
                 "related_document": document.id,
                 "set_active": serializer.validated_data.get("set_active")},
                 status=status.HTTP_201_CREATED,
                 headers=headers)
        else:
            return Response(
                {
                    "Error": "Document not found."
                },
                status=status.HTTP_400_BAD_REQUEST
            )
````
При создании ресурса, ресурс привязывается к документу. Привязка происходит в функции [bind_resource_to_document]().
##### <a>Привязка ресурса к документу</a>
При set_active = True созданный ресурс становится активной версией в документе.
````
def bind_resource_to_document(document: Document, file,
                              creator_id, set_active: bool):
    """Привязывает ресурс к документу."""
    resource = DocumentResource.objects.create(
        related_document=document,
        file=file,
        creator=creator_id
    )
    document.resources.add(resource)
    if set_active:
        document.active_version = resource
        document.save()
    return resource
````
#### <a>Удаление ресурса</a>
````
class DestroyDocumentResourceAPIView(TokenAuthorizationMixin, generics.DestroyAPIView):
    """Удаление ресурса документа.\n
    По эндпоинту "/api/document/resource/deleting/{id}"
    удаляется ресурс документа.\n
    В пути запроса указывается {id} ресурса, который нужно удалить.\n
    Доступ: создателю документа.\n
    """
    queryset = DocumentResource.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsCreator,)

````
#### <a>Изменение ресурса</a>
При изменении ресурса меняется документ в котором он находится. Изменение связи документ ресурса происходит в функции [rebind_resource_to_document]().
````
class RebindDocumentResource(TokenAuthorizationMixin, generics.UpdateAPIView):
    """Изменение документ ресурса.\n
    По эндпоинту "/api/document/resource/rebind/{id}"
    изменяется документ ресурса.\n
    В пути запроса указывается {id} ресурса, который нужно изменить.\n
    Доступ: создателю ресурса.\n
    """
    queryset = DocumentResource.objects.all()
    serializer_class = RebindDocumentResourceSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsCreator,)

    def update(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        resource = self.get_object()
        document = Document.objects.filter(
            pk=serializer.validated_data.get("document")).first()
        if not document:
            return Response(
                data={"Error": "Document with id ="
                      f"'{serializer.validated_data.get('document')}'"
                      "not found."},
                status=status.HTTP_400_BAD_REQUEST
            )
        rebind_resource_to_document(
            document=document,
            resource=resource,
            set_active=serializer.validated_data.get("set_active")
        )
        return Response(
            data=resource.to_dict(),
            status=status.HTTP_200_OK
        )

    def put(self, request, **kwargs):
        return self.update(request, **kwargs)

    def patch(self, request, **kwargs):
        return self.partial_update(request, **kwargs)
````
##### <a>Изменение связи ресурс документ</a>
````
def rebind_resource_to_document(document: Document,
                                resource: DocumentResource,
                                set_active: bool):
    """Удаляет ресурс с документа и привязывает его к новому
    документу."""
    current_document = Document.objects.filter(
        pk=str(resource.related_document)).first()
    if current_document:
        resource.related_document = document
        resource.save()
        current_document.resources.remove(resource)
        document.resources.add(resource)
        if set_active:
            document.active_version = resource
            document.save()
        return resource
    return None
````
* ### <a>Папка</a>
#### <a>Создание папки</a>
````
class FolderCreateAPIView(TokenAuthorizationMixin, generics.CreateAPIView):
    """Создание папки.\n
    По эндпоинту "/api/folder/create" папка создаётся без расположения в папке,
    то есть на главной странице пользователя.\n
    По эндпоинту "/api/folder/create-in-folder/{id}"
    новая папка создаётся в папке.
    В пути запроса указывается {id} папки, в которой создаётся новая папка.\n
    Доступ: все авторизованные пользователи.\n
    """
    serializer_class = FolderCreateSerializer
    queryset = Folder.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        if kwargs:
            location = kwargs["pk"]
        else:
            location = None
        if Folder.objects.filter(
            name=serializer.validated_data.get("name"),
                location=location).exists():
            return Response(
                data={"Error": "Folder with name already"
                      "exists in this folder."},
                status=status.HTTP_400_BAD_REQUEST
            )
        folder = Folder.objects.create(
            name=serializer.validated_data.get("name"),
            creator=self.request.user.id,
            location=location
        )
        return Response(folder.to_dict(),
                        status=status.HTTP_201_CREATED)
````
#### <a>Просмотр папки</a>
Отображение содержимого папки по его ID.
````
class GetFolderByIdAPIView(TokenAuthorizationMixin, generics.RetrieveAPIView):
    """Отображение папки.\n
    По эндпоинту "/api/folder/getting/{id}" отображается содержимое папки.\n
    В пути запроса указывается {id} папки, которую нужно отобразить.\n
    В папке отображаются только те документы и папки,
    которые в ней находятся.\n
    Доступ: создатель папки или разрешенные пользователи.\n
    """
    serializer_class = FoldersAndDocumentsSerializer
    queryset = Folder.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsCreatorOrAllowedUser,)

    def get(self, *args, **kwargs):
        obj = self.get_object()
        folders = Folder.objects.all().filter(location=str(obj))
        documents = Document.objects.all().filter(folder=str(obj))
        serializer = self.serializer_class(
            data={"folders": list(folders.values("id", "name")),
                  "documents": list(documents.values("id", "name"))}
        )
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
````
Отображение папок и документов пользователя по его ID. Отображаются те документы и папки, у которых folder и location is null(на главном экране).
````
class GetUserFoldersDocumentsAPIView(TokenAuthorizationMixin, generics.RetrieveAPIView):
    """Отображение документов и папок пользователя.\n
    По эндпоинту "/api/folder/getting/user/{id}" отображаются все документы и
    папки пользователя, которые находятся на главной странице
    (те, которые не находятся в папках).\n
    В пути запроса указывается {id} пользователя, документы и папки, которого
    нужно отобразить.\n
    Доступ: зарегистрированный пользователь.\n
    """
    serializer_class = FoldersAndDocumentsSerializer
    queryset = User.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, *args, **kwargs):
        creator = self.get_object()
        folders = Folder.objects.all().filter(creator=creator.id,
                                              location=None)
        documents = Document.objects.all().filter(creator=creator.id,
                                                  folder=None)
        serializer = self.serializer_class(
            data={"folders": list(folders.values("id", "name")),
                  "documents": list(documents.values("id", "name"))}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

````
#### <a>Удаление папки</a>
Для удаления папки необходимо предварительно очистить его содержимое.
````
class DestroyFolderAPIView(TokenAuthorizationMixin, generics.DestroyAPIView):
    """Удаление папки.\n
    По эндпоинту "/api/folder/deleting/{id}" удаляется папка.\n
    В пути запроса указывается {id} папки, которую нужно удалить.\n
    Доступ: создателю папки.\n
    """
    queryset = Folder.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsCreator,)

    def delete(self, request, **kwargs):
        delete_folder = self.get_object()
        folders_in_delete_folder = Folder.objects.all().filter(
            location=delete_folder.id).first()
        if delete_folder.documents.all() or folders_in_delete_folder:
            return Response(data={
                "Error": f"Сlear the contents of the folder{delete_folder.id},"
                "deletion is not possible."},
                status=status.HTTP_400_BAD_REQUEST
            )
        delete_folder.delete()
        return Response(data={"Done": "The folder has been deleted."},
                        status=status.HTTP_204_NO_CONTENT)
````
#### <a>Изменение папки</a>
Изменяет название папки.
````
class FolderUpdateAPIView(TokenAuthorizationMixin, generics.UpdateAPIView):
    """Изменение папки.\n
    По эндпоинту "/api/folder/updating/{id}" изменяется папка.\n
    В пути запроса указывается {id} папки, которую нужно изменить.\n
    Доступ: создателю папки.\n
    """
    serializer_class = FolderUpdateSerializer
    queryset = Folder.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsCreator,)

    def update(self, request, **kwargs):
        partial = kwargs.pop('partial', False)
        folder = self.get_object()
        serializer = self.serializer_class(folder,
                                           data=request.data,
                                           partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
                folder.to_dict(),
                status=status.HTTP_200_OK)

    def put(self, request, **kwargs):
        return self.update(request, **kwargs)

    def patch(self, request, **kwargs):
        return self.partial_update(request, **kwargs)
````
* ### <a>Разрешение</a>
#### <a>Создание разрешения</a>
Создаёт разрешение пользователю доступ к документу. Добавляет в allowed_user документа выбранного пользователя.
````
class CreateDocumentPermissionAPIView(TokenAuthorizationMixin, generics.CreateAPIView):
    """Создание доступа к документу.\n
    По эндпоинту "/api/permission/create/document/{id}" создаётся доступ
    для пользователя к документу.\n
    В пути запроса указывается {id} документа, к которому нужно дать доступ.\n
    В теле запроса указывается {id} пользователя, которому нужно дать доступ.\n
    Доступ: создатель документа.
    """
    queryset = Document.objects.all()
    serializer_class = DocumentPermissionSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsCreator,)

    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        document = self.get_object()
        user = serializer.validated_data.get("user")
        if DocumentPermission.objects.filter(document=document,
                                             user=user).exists():
            return Response(data={"error":
                                  "The user already have"
                                  "permission to this document."},
                            status=status.HTTP_400_BAD_REQUEST)
        if document.creator == user.id:
            return Response(data={"error":
                                  "You can't set permission for creator."},
                            status=status.HTTP_400_BAD_REQUEST)
        permission = DocumentPermission(document=document,
                                        user=user,
                                        creator=self.request.user.id)
        permission.save()
        document.allowed_user.add(permission)
        return Response(data={"user": user.id, "document": document.id},
                        status=status.HTTP_201_CREATED)
````
Создаёт разрешение пользователю доступ к папке. Добавляет в allowed_user папки выбранного пользователя.
````
class CreateFolderPermissionAPIView(TokenAuthorizationMixin, generics.CreateAPIView):
    """Создание доступа к папке.\n
    По эндпоинту "/api/permission/create/folder/{id}" создаётся доступ
    для пользователя к папке.\n
    В пути запроса указывается {id} папки, к которой нужно дать доступ.\n
    В теле запроса указывается {id} пользователя, которому нужно дать доступ.\n
    Доступ: создатель папки.
    """
    queryset = Folder.objects.all()
    serializer_class = FolderPermissionSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsCreator,)

    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        folder = self.get_object()
        user = serializer.validated_data.get("user")
        if FolderPermission.objects.filter(folder=folder, user=user).exists():
            return Response(data={"error":
                                  "The user already have"
                                  "permission to this folder."},
                            status=status.HTTP_400_BAD_REQUEST)
        if folder.creator == user.id:
            return Response(data={"error":
                                  "You can't set permission for creator"},
                            status=status.HTTP_400_BAD_REQUEST)
        permission = FolderPermission(folder=folder,
                                      user=user,
                                      creator=self.request.user.id)
        permission.save()
        folder.allowed_user.add(permission)
        return Response(data={"user": user.id, "folder": folder.id},
                        status=status.HTTP_201_CREATED)
````
#### <a>Удаление разрешения</a>
Удаляет разрешение на просмотр документа у выбранного пользователя.
````
class DeleteDocumentPermissionAPIView(TokenAuthorizationMixin, generics.DestroyAPIView):
    """Удаление доступа к документу.\n
    По эндпоинту "/api/permission/delete/document/{id}" удаляется доступ
    к документу.\n
    В пути запроса указывается {id} обьекта DocumentPermission,
    который нужно удалить.\n
    Доступ: создателю документа.\n
    """
    queryset = DocumentPermission.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsCreator,)

    def delete(self, request, pk):
        permission = self.get_object()
        document = permission.document
        if document.creator != self.request.user.id:
            return Response(data={"error": "Document permission can"
                                  "create only document's creator"},
                            status=status.HTTP_400_BAD_REQUEST)
        document.allowed_user.remove(permission)
        permission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
````
Удаляет разрешение на просмотр папки у выбранного пользователя.
````
class DeleteFolderPermissionAPIView(TokenAuthorizationMixin, generics.DestroyAPIView):
    """Удаление доступа к папке.\n
    По эндпоинту "/api/permission/delete/folder/{id}" удаляется доступ
    к папке.\n
    В пути запроса указывается {id} обьекта FolderPermission,
    который нужно удалить.\n
    Доступ: создателю папки.\n
    """
    queryset = FolderPermission.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsCreator,)

    def delete(self, request, pk):
        permission = self.get_object()
        folder = permission.folder
        if folder.creator != self.request.user.id:
            return Response(
                data={"error": "Folder permission"
                               "can create only folder's creator"},
                status=status.HTTP_400_BAD_REQUEST)
        folder.allowed_user.remove(permission)
        permission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
````
#### <a>Просмотр разрешения</a>
Выводит список всех разрешенных пользователей у документа.
````
class GetDocumentPermissionAPIView(TokenAuthorizationMixin, generics.ListAPIView):
    """Отображение доступа к документу.\n
    По эндпоинту "/api/permission/get/document/{id}" отображается
    список пользователей у которых есть доступ к документу.\n
    В пути запроса указывается {id} документа, к которому будет выведен
    список разрешенных пользователей.\n
    Доступ: создатель документа.
    """
    queryset = Document.objects.all()
    serializer_class = DocumentPermissionSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsCreator,)

    def get(self, request, *args, **kwargs):
        document = self.get_object()
        users = DocumentPermission.objects.filter(
            document=document).values("user")
        if not document:
            return Response({"message": "Document not found."},
                            status=status.HTTP_404_NOT_FOUND)
        permission = DocumentPermission.objects.filter(
            document=document).values("user", "document")
        if not permission:
            return Response({"message": "Permission not found."},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(data=list(users), many=True)
        serializer.is_valid(raise_exception=True)
        return Response(list(users), status=status.HTTP_200_OK)
````
Выводит список всех разрешенных пользователей у папки.
````
class GetFolderPermissionAPIView(TokenAuthorizationMixin, generics.ListAPIView):
    """Отображение доступа к папке.\n
    По эндпоинту "/api/permission/get/folder/{id}" отображается
    список пользователей у которых есть доступ к папке.\n
    В пути запроса указывается {id} папки, к которой будет выведен
    список разрешенных пользователей.\n
    Доступ: создатель папки.
    """
    queryset = Folder.objects.all()
    serializer_class = FolderPermissionSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsCreator,)

    def get(self, request, *args, **kwargs):
        folder = self.get_object()
        users = FolderPermission.objects.filter(folder=folder).values("user")
        if not folder:
            return Response({"message": "Folder not found."},
                            status=status.HTTP_404_NOT_FOUND)
        permission = FolderPermission.objects.filter(
            folder=folder).values("user", "folder")
        if not permission:
            return Response({"message": "Permission not found."},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(data=list(users), many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

````
## <a>Панель админа</a>
* ### <a>Документы</a>
Отображаются UUID документов, их названия, расположение документов, UUID создателя, дата создания.
![image](https://github.com/Mans-Mans/hw_python_oop/assets/118307945/966974bc-6926-4b60-a72c-b9045ec60f4d)
* ### <a>Документ ресурсы</a>
Отображаются UUID ресурсов, их названия, документ в котором он находится, UUID создателя, дата создания.
![image](https://github.com/Mans-Mans/hw_python_oop/assets/118307945/3a0fdf58-9d46-42e4-b9a1-6243a4035a8f)
* ### <a>Папки</a>
Отображаются UUID папок, их названия, расположение папок, UUID создателя, дата создания.
![image](https://github.com/Mans-Mans/hw_python_oop/assets/118307945/19354010-0021-4576-abc6-d99b130a2cc9)
* ### <a>Разрешение документов</a>
Отображаются UUID разрешений, UUID документа, email пользователя, UUID создателя, дата создания.
![image](https://github.com/Mans-Mans/hw_python_oop/assets/118307945/d2fbdb06-6d46-4835-8a9f-b0d1705d28c4)
* ### <a>Разрешение папок</a>
Отображаются UUID разрешений, UUID папки, email пользователя, UUID создателя, дата создания.
![image](https://github.com/Mans-Mans/hw_python_oop/assets/118307945/98c07469-c2c5-4426-8bba-f3afdd327125)

## <a>Инструкция запуска сервера локально</a>
Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@gitlab.it-psg.com:ib-elp-it-psg/documents_management_module.git
```
Cоздать и активировать виртуальное окружение:
```
python -m venv venv
```
* Если у вас Linux/macOS
    ```
    source env/bin/activate
    ```
* Если у вас windows
    ```
    source venv/scripts/activate
    ```
```
python -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Перейдите в директорию с файлом manage.py
```
cd documents_module
```
Создайте файл .env:
```
touch .env
```
Заполните его по примеру env_example:
```
DEBUG=True
SECRET_KEY=django-insecure-_0x8o11zqs28yhn@7aqea&hf=l@(*m(db$6kz7fu@m5rsfsf)    # change
MODULE_TOKEN=feb77714869835a08fbd2a82c133344bd99b160b   # change
DATABASE_NAME=YourDBName   # change
DATABASE_USERNAME=YourUsername   # change
DATABASE_PASSWORD=YourPassword   # change
DATABASE_HOST=localhost
DATABASE_PORT=5432
```
Перейдите в директорию settings и создайте там local_settings.py:
```
cd documents_module/settings
touch local_settings.py
```
Заполните его по примеру с local_settings.example:
```
DEBUG = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': your_database_name,     # change database name
        'USER': username,     # change user
        'PASSWORD': db_password,      # secure password
        'HOST': db_host,    # change host
        'PORT': db_host
    }
}
```
Перейдите в директорию где лежит manage.py и выполните миграции:
```
cd ../..
python manage.py makemigrations
python manage.py migrate
```
Создайте суперюзера. Придумайте пароль и логин:
```
python manage.py createsuperuser
```
Запустите сервер:
```
python manage.py runserver
```
## <a>Инструкция запуска удаленно на сервере</a>

## <a>API</a>
* ### <a>Статическая API документация</a>
Статическая API документация находится по [ссылке](https://gitlab.it-psg.com/ib-elp-it-psg/documents_management_module/-/blob/develop/documents_module/documents_module/api_docs/schema.yaml?ref_type=heads). Для более комфортного чтения API рекомендуется использовать online [swagger editor](https://editor.swagger.io). Для этого необходимо скопировать содержимое файла и вставить в [swagger editor](https://editor.swagger.io).
* ### <a>Динамическая API документация</a>
Динамическая документация рекомендована для работы в режиме разработки. Для просмотра динамической API документации необходимо предварительно [запустить сервер](#инструкция-запуска-сервера-локально). Далее документация будет доступна в удобно читаемом формате по эндпоинту http://127.0.0.1:8000/api/redoc/ .
* ### <a>Инструкция по работе с API</a>
