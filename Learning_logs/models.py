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
    date_added=models.DateTimeField(auto_now=True)
    last_modified = models.DateTimeField(auto_now_add=True)  #auto_now takes precedence (obviously, because it updates field each time, while auto_now_add updates on creation only.
    # So making last_modified as auto_now_add Does not automatically update time on each save. But rather updates on creation(new entry is created when change is detected) only.
    def save(self, *args, **kwargs):
        if self.pk:  # Check if it's an existing entry
            # Fetch the existing entry from the database
            original_entry = Entry.objects.get(pk=self.pk)
            if original_entry.text != self.text:
                # Save the original entry's timestamp in the past version
                EntryHistory.objects.create(
                    entry=self,
                    text=original_entry.text,
                    date_created=original_entry.date_added
                )
        super().save(*args, **kwargs)
    
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
class EntryHistory(models.Model):
    entry = models.ForeignKey(Entry, related_name='history', on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField()