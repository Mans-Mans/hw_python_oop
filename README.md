# Руководство разработчика
## Оглавление 
* [Модели](#модели)
  * [Документ](#документ)
  * [Ресурс документа](#ресурс-документа)
    * [Путь к файлу](#путь-к-файлу)
  * [Папка](#папка)
  * [Разрешение документа](#разрешение-документа)
  * [РазрешениеПапки](#разрешение-папки)
* [Сериализаторы]
  * [Документ]
  * [Папка]
  * [Разрешение]
* [View функции]
  * [Документ]
    * [Создание документа]
    * [Просмотр документа]
    * [Удаление документа]
    * [Редактирование документа]
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
### <a>Документ</a>
````
class Document(UUIDModel):
    """Модель документа.\n
    Обьект этой модели вернет его UUID.
    Значение folder хранит UUID папки, в которой распологается документ.
    Если folder is None значит документ находися на главной странице
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
### <a>Ресурс Документа</a>
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
````
def document_resource_file_path(instance, filename):
    name, extension = os.path.splitext(filename)
    return 'media/documents/{0}/{1}{2}'.format(
        instance.related_document.pk,
        f"{str(name)}{datetime.now().strftime('%Y%m%d%H%M%S')}",
        str(extension)
    )
````
### <a>Папка</a>
````
class Folder(UUIDModel):
    """Модель папки.\n
    Обьект модели возвращает его PK.\n
    Значение location хранит UUID папки, в которой распологается текущая
    папка. Если location пустая значит папка находися на главной странице
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
### <a>Разрешение документа</a>
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
### <a>Разрешение папки</a>
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
## <a>Использованные методы</a>
### <a>Путь до файла</a>
