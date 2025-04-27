from structures.models import MemoryInput, MemoryResult

def extract_memory(memory_input: MemoryInput) -> MemoryResult:
    """
    summarizes the memory for an iteration and returns the MemoryResult object.
   
     """
    if memory_input.iteration ==0:
        return MemoryResult(result="No past interactions available.")
    past_interaction = f'''in the iteration {memory_input.iteration + 1}, you called '{memory_input.function_name}' with arguments: {memory_input.arguments}. The function returned: {memory_input.result}'''
    return MemoryResult(memory=past_interaction)
    
    

#example usage of the function
if __name__ == "__main__":
    memory_input = MemoryInput(
        iteration=1,
        function_name="get_weather",
        arguments={"location": "New York"},
        result="Sunny, 25°C",
        response="The weather information is retrieved successfully."
    )
    
    memory_result = extract_memory(memory_input)
    print(memory_result)  # Output: In iteration 2, you called 'get_weather' with arguments: {'location': 'New York'}. The function returned: Sunny, 25°C