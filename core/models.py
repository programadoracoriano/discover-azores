from django.db import models
from django_resized import ResizedImageField
from ckeditor.fields import RichTextField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',
                                       verbose_name="Utilizador", null=True, blank=True)
    image       = ResizedImageField(size=[200, 200], upload_to='users/profile/', force_format='WEBP',
                                    quality=85, null=True, blank=True, verbose_name="Foto de Perfil",
                                    keep_meta=False)
    address     = models.CharField(max_length=150, null=True, blank=True,
                                   verbose_name="Morada")
    zip_code    = models.CharField(max_length=150, null=True, blank=True,
                                   verbose_name="Código Postal")
    city        = models.CharField(max_length=150, null=True, blank=True,
                                   verbose_name="Cidade")
    verified    = models.CharField(max_length=1, null=True, blank=True, default=0,
                                   verbose_name="Verificado")

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class ImageGallery(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name="Utilizador")
    name    = models.CharField(max_length=150, null=False, blank=False,
                               verbose_name="Nome da Foto")
    image   = ResizedImageField(upload_to='gallery/', force_format='WEBP',
                                    quality=85, null=True, blank=True, verbose_name="Imagem",
                                    keep_meta=False)

    @property
    def image_url(self):
        return "{0}{1}".format(settings.SITE_URL, self.image.url)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name        = 'Galeria'
        verbose_name_plural = 'Galeria'

class Island(models.Model):
    name            = models.CharField(max_length=150, null=False, blank=False, verbose_name="Nome da Ilha")
    image           = ResizedImageField(size=[200, 200], upload_to='islands/images/', force_format='WEBP',
                                    quality=85, null=True, blank=True, verbose_name="Imagem",
                                    keep_meta=False)
    cover           = ResizedImageField(upload_to='islands/covers/', force_format='WEBP',
                                    quality=85, null=True, blank=True, verbose_name="Imagem de Capa",
                                    keep_meta=False)
    description_pt  = RichTextField(verbose_name="Descrição(Português)", null=True, blank=True)
    description_en  = RichTextField(verbose_name="Descrição(Inglês)", null=True, blank=True)
    gallery         = models.ManyToManyField(ImageGallery, blank=True)
    vidId           = models.CharField(max_length=150, null=True, blank=True, verbose_name="Id de Video")

    @property
    def logo_url(self):
        return "{0}{1}".format(settings.SITE_URL, self.image.url)

    @property
    def cover_url(self):
        if self.cover:
            return "{0}{1}".format(settings.SITE_URL, self.cover.url)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ilha'
        verbose_name_plural = 'Ilhas'

class County(models.Model):
    name            = models.CharField(max_length=150, null=False, blank=False, verbose_name="Nome do Concelho")
    island          = models.ForeignKey(Island, null=True, blank=False, verbose_name="Ilha", on_delete=models.CASCADE)
    image           = ResizedImageField(size=[200, 200], upload_to='county/images/', force_format='WEBP',
                                    quality=85, null=True, blank=True, verbose_name="Imagem",
                                    keep_meta=False)
    cover           = ResizedImageField(upload_to='county/covers/', force_format='WEBP',
                                    quality=85, null=True, blank=True, verbose_name="Imagem de capa",
                                    keep_meta=False)
    description_pt  = RichTextField(verbose_name="Descrição(Português)", null=True, blank=True)
    description_en  = RichTextField(verbose_name="Descrição(Inglês)", null=True, blank=True)
    gallery         = models.ManyToManyField(ImageGallery, blank=True)
    date_founded    = models.DateField(null=True, blank=True, verbose_name="Data de Fundação")
    vidId           = models.CharField(max_length=150, null=True, blank=True, verbose_name="Id de Video")

    @property
    def logo_url(self):
        return "{0}{1}".format(settings.SITE_URL, self.logo.url)

    @property
    def cover_url(self):
        if self.cover:
            return "{0}{1}".format(settings.SITE_URL, self.cover.url)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Concelho'
        verbose_name_plural = 'Concelhos'

class Parish(models.Model):
    name            = models.CharField(max_length=150, null=False, blank=False, verbose_name="Nome da Freguesia")
    county          = models.ForeignKey(County, null=False, blank=False, verbose_name="Concelho",
                                        on_delete=models.CASCADE)
    image           = ResizedImageField(size=[200, 200], upload_to='parish/images/', force_format='WEBP',
                                    quality=85, null=True, blank=True, verbose_name="Imagem",
                                    keep_meta=False)
    cover           = ResizedImageField(size=[200, 200], upload_to='parish/covers/', force_format='WEBP',
                                    quality=85, null=True, blank=True, verbose_name="Imagem de capa",
                                    keep_meta=False)
    description_pt  = RichTextField(verbose_name="Descrição(Português)", null=True, blank=True)
    description_en  = RichTextField(verbose_name="Descrição(Inglês)", null=True, blank=True)
    gallery         = models.ManyToManyField(ImageGallery, blank=True)
    date_founded    = models.DateField(null=True, blank=True, verbose_name="Data de Fundação")
    vidId           = models.CharField(max_length=150, null=True, blank=True, verbose_name="Id de Video")

    @property
    def logo_url(self):
        return "{0}{1}".format(settings.SITE_URL, self.logo.url)

    @property
    def cover_url(self):
        if self.cover:
            return "{0}{1}".format(settings.SITE_URL, self.cover.url)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Freguesia'
        verbose_name_plural = 'Freguesias'

class PlaceCategorie(models.Model):
    categorie_pt = models.CharField(max_length=150, null=True, blank=False, verbose_name="Categoria(Português)")
    categorie_en = models.CharField(max_length=150, null=True, blank=False, verbose_name="Categoria(Inglês)")
    class Meta:
        verbose_name = 'Categoria de Locais'
        verbose_name_plural = 'Categorias de Locais'
    def __str__(self):
        return self.categorie_pt

class PlaceSubCategorie(models.Model):
    subcategorie_pt     = models.CharField(max_length=150, null=True, blank=False, verbose_name="Sub Categoria(Português)")
    subcategorie_en     = models.CharField(max_length=150, null=True, blank=False, verbose_name="Sub Categoria(Inglês)")
    categorie           = models.ForeignKey(PlaceCategorie, null=False, blank=False, verbose_name="Categoria", on_delete=models.CASCADE)

    def __str__(self):
        return self.subcategorie_pt

    class Meta:
        verbose_name = 'Subcategoria de Locais'
        verbose_name_plural = 'Subcategorias de Locais'

class PlaceTag(models.Model):
    tag_pt = models.CharField(max_length=150, null=False, blank=False, verbose_name="Tag(Português)")
    tag_en = models.CharField(max_length=150, null=False, blank=False, verbose_name="Tag(Inglês)")

    def __str__(self):
        return self.flare_pt
    class Meta:
        verbose_name = 'Tag para local'
        verbose_name_plural = 'Tags para Locais'

class Food(models.Model):
    name            = models.CharField(max_length=150, null=False, blank=False, verbose_name="Nome da Comida")
    description_pt  = RichTextField(verbose_name="Descrição(Português)", null=True, blank=True)
    description_en  = RichTextField(verbose_name="Descrição(Inglês)", null=True, blank=True)
    image           = ResizedImageField(upload_to='food/images/', force_format='WEBP',
                                    quality=85, null=True, blank=True, verbose_name="Imagem",
                                    keep_meta=False)
    gallery         = models.ManyToManyField(ImageGallery, blank=True)

    @property
    def image_url(self):
        return "{0}{1}".format(settings.SITE_URL, self.image.url)

    def __str__(self):
        return self.name

class Place(models.Model):
    name            = models.CharField(max_length=150, null=False, blank=False, verbose_name="Nome")
    user            = models.ForeignKey(User, null=True, blank=True, verbose_name="Utilizador",
                                        on_delete=models.CASCADE)
    slug            = models.CharField(max_length=150, null=True, blank=True, verbose_name="Slug", unique=True)
    parish          = models.ForeignKey(Parish, null=False, blank=False, verbose_name="Freguesia",
                                        on_delete=models.CASCADE)
    categorie       = models.ForeignKey(PlaceSubCategorie, null=False, blank=False, verbose_name="Categoria",
                                        on_delete=models.CASCADE)
    stars           = models.IntegerField(null=True, blank=True, verbose_name="Estrelas(Se for Hotel)")
    description_pt  = RichTextField(verbose_name="Descrição(Português)", null=True, blank=True)
    description_en  = RichTextField(verbose_name="Descrição(Inglês)", null=True, blank=True)
    image           = ResizedImageField(size=[1024, 768], quality=85, keep_meta=False,
                                            null=True, blank=False,
                                            upload_to='places/images', force_format='WEBP')
    cover           = ResizedImageField(quality=85, keep_meta=False,
                                            null=True, blank=False,
                                            upload_to='places/covers', force_format='WEBP')
    address         = models.CharField(max_length=300, null=True, blank=True, verbose_name="Morada")
    zip_code        = models.CharField(max_length=12, null=True, blank=True, verbose_name="Código Postal")
    map_lat         = models.CharField(max_length=150, null=True, blank=True, verbose_name="Latitude(Mapa)")
    map_long        = models.CharField(max_length=150, null=True, blank=True, verbose_name="Longitude(Mapa)")
    phone_number    = models.CharField(max_length=12, null=True, blank=True, verbose_name="Número de Telefone")
    email           = models.EmailField(null=True, blank=True, verbose_name="E-mail")
    food            = models.ManyToManyField(Food, blank=True, verbose_name="Comida(Se for restaurante)")
    gallery         = models.ManyToManyField(ImageGallery, blank=True)
    tag             = models.ManyToManyField(PlaceTag, blank=True)
    site            = models.URLField(null=True, blank=True, verbose_name="Site")
    trip_advisor    = models.URLField(null=True, blank=True, verbose_name="Trip Advisor")
    booking         = models.URLField(null=True, blank=True, verbose_name="Booking")
    facebook        = models.URLField(null=True, blank=True, verbose_name="Facebook")
    instagram       = models.URLField(null=True, blank=True, verbose_name="Instagram")
    vidId           = models.CharField(max_length=150, null=True, blank=True, verbose_name="Id de Video(Youtube)")
    published       = models.CharField(max_length=1, null=True, blank=True, default=0, verbose_name="Publicado")
    def __str__(self):
        return self.name

    @property
    def image_url(self):
        return "{0}{1}".format(settings.SITE_URL, self.image.url)

    @property
    def cover_url(self):
        if self.cover:
            return "{0}{1}".format(settings.SITE_URL, self.cover.url)

    class Meta:
        verbose_name = 'Local'
        verbose_name_plural = 'Locais'
