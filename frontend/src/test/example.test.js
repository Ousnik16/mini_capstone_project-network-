import { describe, it, expect,vi } from 'vitest';




describe('Example Test Suite', () => {
  describe('Basic Assertions', () => {
    it('should perform basic equality checks', () => {
      expect(2 + 2).toBe(4);
      expect([1, 2, 3]).toHaveLength(3);
      expect('hello').toContain('hell');
    });

    it('should handle truthy/falsy checks', () => {
      expect(true).toBe(true);
      expect(null).toBeNull();
      expect(undefined).toBeUndefined();
      expect('').toBeFalsy();
      expect('text').toBeTruthy();
    });

    it('should compare objects and arrays', () => {
      const obj = { a: 1, b: 2 };
      expect(obj).toEqual({ a: 1, b: 2 });
      expect([1, 2, 3]).toEqual([1, 2, 3]);
    });
  });

  describe('Mock Functions', () => {
    it('should track function calls', () => {
      const mockFn = vi.fn();
      mockFn('test');
      
      expect(mockFn).toHaveBeenCalled();
      expect(mockFn).toHaveBeenCalledWith('test');
      expect(mockFn).toHaveBeenCalledTimes(1);
    });

    it('should return mock values', () => {
      const mockFn = vi.fn().mockReturnValue('test-value');
      const result = mockFn();
      
      expect(result).toBe('test-value');
    });

    it('should handle async mock functions', async () => {
      const mockFn = vi.fn().mockResolvedValue({ id: 1, name: 'Test' });
      const result = await mockFn();
      
      expect(result).toEqual({ id: 1, name: 'Test' });
    });
  });

  describe('Async Testing', () => {
    it('should handle promises', async () => {
      const promise = Promise.resolve('success');
      await expect(promise).resolves.toBe('success');
    });

    it('should handle rejected promises', async () => {
      const promise = Promise.reject(new Error('test error'));
      await expect(promise).rejects.toThrow('test error');
    });
  });

  describe('Error Handling', () => {
    it('should catch thrown errors', () => {
      const throwError = () => {
        throw new Error('Something went wrong');
      };
      
      expect(throwError).toThrow('Something went wrong');
    });

    it('should verify error types', () => {
      const throwError = () => {
        throw new TypeError('Invalid type');
      };
      
      expect(throwError).toThrow(TypeError);
    });
  });
});
