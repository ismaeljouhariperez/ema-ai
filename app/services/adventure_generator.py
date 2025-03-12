from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.chains import LLMChain
from app.core.config import settings
from app.models.adventure import Adventure
from app.core.exceptions import PromptProcessingError, OpenAIError, InvalidPromptError
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential
import openai

class AdventureGenerator:
    """Service pour générer des aventures à partir de prompts utilisateurs"""
    
    def __init__(self):
        # Initialiser le modèle OpenAI
        self.llm = ChatOpenAI(
            model_name=settings.OPENAI_MODEL,
            temperature=0.7,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Créer le parser pour formater la sortie en objet Adventure
        self.parser = PydanticOutputParser(pydantic_object=Adventure)
        
        # Définir le template de prompt
        template = """
        Tu es un expert en micro-aventures et activités de plein air en France. 
        Ton rôle est de générer des suggestions d'aventures personnalisées basées sur les demandes des utilisateurs.
        
        Voici la demande de l'utilisateur : {prompt}
        
        Analyse cette demande et génère une micro-aventure adaptée avec les caractéristiques suivantes :
        - Un titre accrocheur
        - Une description détaillée et inspirante
        - Un lieu précis en France
        - Des tags pertinents (activité, environnement, saison, etc.)
        - Un niveau de difficulté (facile, moyen, difficile)
        - Une durée estimée en minutes
        - Une distance en kilomètres
        - Des coordonnées géographiques précises (latitude et longitude)
        
        Réponds UNIQUEMENT avec un objet JSON valide suivant ce format exact, sans texte supplémentaire :
        {format_instructions}
        """
        
        # Créer le prompt avec les instructions de formatage
        self.prompt = ChatPromptTemplate.from_template(
            template=template,
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        
        # Créer la chaîne LLM
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def generate_adventure(self, prompt: str) -> Adventure:
        """
        Génère une aventure à partir d'un prompt utilisateur
        
        Args:
            prompt: Le prompt utilisateur décrivant l'aventure souhaitée
            
        Returns:
            Un objet Adventure contenant les détails de l'aventure générée
            
        Raises:
            InvalidPromptError: Si le prompt est vide ou invalide
            OpenAIError: Si une erreur se produit avec l'API OpenAI
            PromptProcessingError: Si une erreur se produit lors du traitement du prompt
        """
        try:
            # Valider le prompt
            if not prompt or len(prompt.strip()) < 5:
                raise InvalidPromptError("Le prompt doit contenir au moins 5 caractères")
                
            logger.info(f"Génération d'une aventure pour le prompt: {prompt}")
            
            # Exécuter la chaîne LLM
            result = await self.chain.arun(prompt=prompt)
            
            # Parser le résultat en objet Adventure
            adventure = self.parser.parse(result)
            
            logger.info(f"Aventure générée avec succès: {adventure.title}")
            return adventure
            
        except openai.OpenAIError as e:
            logger.error(f"Erreur OpenAI lors de la génération de l'aventure: {str(e)}")
            raise OpenAIError(f"Erreur lors de la communication avec OpenAI: {str(e)}")
        except Exception as e:
            logger.error(f"Erreur lors de la génération de l'aventure: {str(e)}")
            raise PromptProcessingError(f"Erreur lors du traitement du prompt: {str(e)}") 