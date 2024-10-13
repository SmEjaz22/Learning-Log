from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class topic_ofinterest(models.Model):
    """A topic which user selects that user will be learning about."""
    text=models.CharField(max_length=200)
    date_modified=models.DateTimeField(auto_now_add=True)
    owner=models.ForeignKey(User, on_delete=models.CASCADE) #So user own their data.
    def __str__(self):
        return self.text

class Entry(models.Model):  # models.Model means this particular class inherits the django basic model class.
    """something specific we learn from topics"""
    topic=models.ForeignKey(topic_ofinterest,on_delete=models.CASCADE)
    # Means 
    # 
    # on_delete=models.CASCADE argument tells 
    # Django that when a topic is deleted, all the entries associated with that topic 
    # should be deleted as well. This is known as a cascading delete.
    text=models.TextField()
    date_added=models.DateTimeField(auto_now_add=True)

    
    class Meta:
        verbose_name_plural='entries'
        # Means 
        # It will not migrate the database until i wrote verbose_name_plural exactly, don't know yet why.
        
    def __str__(self):
        """Return a simple string represent an entity"""
        if len(self.text)>50:
            return f"{self.text[0:50]}..."
        else:
            return f"{self.text}"
        # Means show 50 characters of text with ... at end.
    